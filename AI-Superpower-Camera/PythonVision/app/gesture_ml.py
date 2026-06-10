from __future__ import annotations

from dataclasses import dataclass
from typing import List

import numpy as np

from .types import FrameData, GestureEvent


@dataclass
class MLClassifierConfig:
    mode: str
    tflite_model_path: str
    onnx_model_path: str


class GestureMLClassifier:
    labels = ["None", "Fireball", "Lightning", "Shield", "EnergyBlast", "Teleport", "Shockwave"]

    def __init__(self, config: MLClassifierConfig):
        self.config = config
        self.backend = None
        self.session = None
        self._init_backend()

    def _init_backend(self) -> None:
        if self.config.mode in ("hybrid", "tflite"):
            try:
                from tflite_runtime.interpreter import Interpreter  # type: ignore
                self.session = Interpreter(model_path=self.config.tflite_model_path)
                self.session.allocate_tensors()
                self.backend = "tflite"
                return
            except Exception:
                pass

            try:
                import tensorflow as tf  # type: ignore
                self.session = tf.lite.Interpreter(model_path=self.config.tflite_model_path)
                self.session.allocate_tensors()
                self.backend = "tflite"
                return
            except Exception:
                pass

        if self.config.mode in ("hybrid", "onnx"):
            try:
                import onnxruntime as ort  # type: ignore
                self.session = ort.InferenceSession(self.config.onnx_model_path)
                self.backend = "onnx"
                return
            except Exception:
                pass

        self.backend = "none"

    def _extract_features(self, frame: FrameData) -> np.ndarray:
        features: List[float] = []
        for lm in frame.pose_landmarks[:33]:
            features.extend([lm.x, lm.y, lm.z])
        for lm in frame.left_hand_landmarks[:21]:
            features.extend([lm.x, lm.y, lm.z])
        for lm in frame.right_hand_landmarks[:21]:
            features.extend([lm.x, lm.y, lm.z])

        target_len = (33 + 21 + 21) * 3
        if len(features) < target_len:
            features.extend([0.0] * (target_len - len(features)))

        features.extend(list(frame.motion.velocity))
        features.extend(list(frame.motion.acceleration))
        return np.array(features, dtype=np.float32)

    def classify(self, frame: FrameData) -> List[GestureEvent]:
        feats = self._extract_features(frame)

        if self.backend == "none":
            return []

        if self.backend == "tflite":
            input_details = self.session.get_input_details()
            output_details = self.session.get_output_details()
            self.session.set_tensor(input_details[0]["index"], feats.reshape(1, -1))
            self.session.invoke()
            scores = self.session.get_tensor(output_details[0]["index"])[0]
        elif self.backend == "onnx":
            input_name = self.session.get_inputs()[0].name
            output_name = self.session.get_outputs()[0].name
            scores = self.session.run([output_name], {input_name: feats.reshape(1, -1)})[0][0]
        else:
            return []

        idx = int(np.argmax(scores))
        conf = float(scores[idx])
        label = self.labels[idx]

        if label == "None" or conf < 0.7:
            return []

        return [GestureEvent(name=label, confidence=conf, timestamp=frame.timestamp)]
