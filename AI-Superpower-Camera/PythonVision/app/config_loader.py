from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import yaml


def load_config(path: str) -> Dict[str, Any]:
    config_path = Path(path).resolve()
    with config_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    base_dir = config_path.parent.parent
    for key in ("sqlite_path", "video_output_dir"):
        rel = data["app"][key]
        data["app"][key] = str((base_dir / rel).resolve())

    for key in ("tflite_model_path", "onnx_model_path"):
        rel = data["ml"][key]
        data["ml"][key] = str((base_dir / rel).resolve())

    return data
