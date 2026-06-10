import time
import sys
from pathlib import Path

sys.path.insert(0, str((Path(__file__).resolve().parents[2] / "PythonVision").resolve()))

from app.types import FrameData


def run_stress(duration_s: int = 30, target_fps: int = 60) -> dict:
    interval = 1.0 / target_fps
    end = time.time() + duration_s
    frames = 0
    while time.time() < end:
        _ = FrameData(timestamp=time.time())
        frames += 1
        time.sleep(interval)
    return {"frames": frames, "avg_fps": frames / duration_s}


if __name__ == "__main__":
    print(run_stress())
