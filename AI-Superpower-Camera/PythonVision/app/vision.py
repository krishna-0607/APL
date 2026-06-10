from __future__ import annotations

import time
from typing import List, Optional

try:
    import cv2
except Exception:  # pragma: no cover
    cv2 = None

try:
    import mediapipe as mp
except Exception:  # pragma: no cover
    mp = None

from .types import FrameData, Landmark, MotionState


class VisionPipeline:
    def __init__(self, config: dict):
        self.config = config
        self._last_head = None
        self._last_velocity = (0.0, 0.0, 0.0)
        self._last_ts = None

        self._cap = None
        self._holistic = None

        if cv2 is not None and mp is not None:
            self._cap = cv2.VideoCapture(config["app"]["camera_index"])
            self._holistic = mp.solutions.holistic.Holistic(
                min_detection_confidence=config["vision"]["min_detection_confidence"],
                min_tracking_confidence=config["vision"]["min_tracking_confidence"],
                model_complexity=1,
            )

    def _to_landmarks(self, source) -> List[Landmark]:
        if source is None:
            return []
        return [Landmark(l.x, l.y, l.z, getattr(l, "visibility", 1.0)) for l in source.landmark]

    def _compute_motion(self, pose_landmarks: List[Landmark], ts: float) -> MotionState:
        if not pose_landmarks:
            return MotionState()

        head = pose_landmarks[0]
        head_vec = (head.x, head.y, head.z)

        if self._last_head is None or self._last_ts is None:
            self._last_head = head_vec
            self._last_ts = ts
            return MotionState()

        dt = max(ts - self._last_ts, 1e-6)
        velocity = tuple((head_vec[i] - self._last_head[i]) / dt for i in range(3))
        acceleration = tuple((velocity[i] - self._last_velocity[i]) / dt for i in range(3))
        norm = max((sum(v * v for v in velocity)) ** 0.5, 1e-6)
        direction = tuple(v / norm for v in velocity)

        self._last_head = head_vec
        self._last_velocity = velocity
        self._last_ts = ts

        return MotionState(velocity=velocity, acceleration=acceleration, direction=direction)

    def read_frame(self) -> Optional[FrameData]:
        ts = time.time()

        if self._cap is None or self._holistic is None:
            return FrameData(timestamp=ts)

        ok, frame = self._cap.read()
        if not ok:
            return None

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self._holistic.process(frame_rgb)

        pose_landmarks = self._to_landmarks(result.pose_landmarks)
        frame_data = FrameData(
            timestamp=ts,
            face_landmarks=self._to_landmarks(result.face_landmarks),
            pose_landmarks=pose_landmarks,
            left_hand_landmarks=self._to_landmarks(result.left_hand_landmarks),
            right_hand_landmarks=self._to_landmarks(result.right_hand_landmarks),
            motion=self._compute_motion(pose_landmarks, ts),
        )

        frame_data.metadata["height"] = float(frame.shape[0])
        frame_data.metadata["width"] = float(frame.shape[1])
        return frame_data

    def close(self) -> None:
        if self._holistic is not None:
            self._holistic.close()
        if self._cap is not None:
            self._cap.release()
