from __future__ import annotations

import hashlib
from typing import Dict


PALETTES = [
    ("#FF5500", "#FFD000"),
    ("#44D9E6", "#0077FF"),
    ("#9A4DFF", "#F84CFF"),
    ("#3CFF7A", "#00B386"),
    ("#FF2E63", "#08D9D6"),
]

PARTICLE_PROFILES = [
    "fire_trail",
    "arc_lightning",
    "energy_wave",
    "shield_pulse",
    "teleport_smoke",
    "shockwave_ring",
]

SOUND_PROFILES = [
    "dragon_roar",
    "electric_surge",
    "energy_charge",
    "shield_hum",
    "teleport_whoosh",
    "impact_boom",
]


def generate_power_profile(name: str) -> Dict[str, str]:
    key = name.strip()
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
    idx = int(digest[:8], 16)

    colors = PALETTES[idx % len(PALETTES)]
    particle_profile = PARTICLE_PROFILES[idx % len(PARTICLE_PROFILES)]
    sound_profile = SOUND_PROFILES[idx % len(SOUND_PROFILES)]

    return {
        "name": key,
        "primary_color": colors[0],
        "secondary_color": colors[1],
        "particle_profile": particle_profile,
        "sound_profile": sound_profile,
    }
