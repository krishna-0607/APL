import time
import sys
from pathlib import Path

sys.path.insert(0, str((Path(__file__).resolve().parents[2] / "PythonVision").resolve()))

from app.power_engine import PowerEngine
from app.types import GestureEvent


def run_perf(iterations: int = 10000) -> dict:
    cfg = {
        "power": {
            "fireball_cooldown_s": 0,
            "lightning_cooldown_s": 0,
            "shield_cooldown_s": 0,
            "energy_blast_cooldown_s": 0,
            "teleport_cooldown_s": 0,
            "shockwave_cooldown_s": 0,
        }
    }
    engine = PowerEngine(cfg)
    evt = GestureEvent(name="Fireball", confidence=0.9, timestamp=time.time())

    start = time.perf_counter()
    for _ in range(iterations):
        engine.trigger(evt)
    elapsed = time.perf_counter() - start

    fps = iterations / elapsed
    return {"iterations": iterations, "elapsed_s": elapsed, "ops_per_s": fps}


if __name__ == "__main__":
    result = run_perf()
    print(result)
