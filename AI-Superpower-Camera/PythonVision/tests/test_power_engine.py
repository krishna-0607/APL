import time
import unittest

from app.power_engine import PowerEngine
from app.types import GestureEvent


class PowerEngineTests(unittest.TestCase):
    def test_cooldown(self):
        cfg = {
            "power": {
                "fireball_cooldown_s": 10,
                "lightning_cooldown_s": 10,
                "shield_cooldown_s": 10,
                "energy_blast_cooldown_s": 10,
                "teleport_cooldown_s": 10,
                "shockwave_cooldown_s": 10,
            }
        }
        engine = PowerEngine(cfg)
        evt = GestureEvent(name="Fireball", confidence=0.9, timestamp=time.time())
        first = engine.trigger(evt)
        second = engine.trigger(evt)
        self.assertEqual(first["type"], "power_trigger")
        self.assertEqual(second["type"], "cooldown")


if __name__ == "__main__":
    unittest.main()
