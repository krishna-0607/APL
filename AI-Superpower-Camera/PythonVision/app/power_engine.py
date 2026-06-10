from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Dict, Optional

from .types import GestureEvent


@dataclass
class PowerState:
    active: bool
    last_triggered_ts: float
    cooldown_s: float


class PowerEngine:
    def __init__(self, config: dict):
        self.power_config = config["power"]
        self.states: Dict[str, PowerState] = {
            "Fireball": PowerState(False, 0.0, self.power_config["fireball_cooldown_s"]),
            "Lightning": PowerState(False, 0.0, self.power_config["lightning_cooldown_s"]),
            "Shield": PowerState(False, 0.0, self.power_config["shield_cooldown_s"]),
            "EnergyBlast": PowerState(False, 0.0, self.power_config["energy_blast_cooldown_s"]),
            "Teleport": PowerState(False, 0.0, self.power_config["teleport_cooldown_s"]),
            "Shockwave": PowerState(False, 0.0, self.power_config["shockwave_cooldown_s"]),
        }

    def trigger(self, gesture: GestureEvent) -> Optional[dict]:
        if gesture.name not in self.states:
            return None

        now = time.time()
        state = self.states[gesture.name]
        remaining = state.cooldown_s - (now - state.last_triggered_ts)
        if remaining > 0:
            return {
                "type": "cooldown",
                "power": gesture.name,
                "remaining": round(remaining, 3),
                "timestamp": now,
            }

        state.active = True
        state.last_triggered_ts = now

        return {
            "type": "power_trigger",
            "power": gesture.name,
            "confidence": gesture.confidence,
            "timestamp": now,
            "state": "active",
        }
