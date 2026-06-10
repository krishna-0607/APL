from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class Landmark:
    x: float
    y: float
    z: float
    visibility: float = 1.0


@dataclass
class MotionState:
    velocity: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    acceleration: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    direction: Tuple[float, float, float] = (0.0, 0.0, 1.0)


@dataclass
class FrameData:
    timestamp: float
    face_landmarks: List[Landmark] = field(default_factory=list)
    pose_landmarks: List[Landmark] = field(default_factory=list)
    left_hand_landmarks: List[Landmark] = field(default_factory=list)
    right_hand_landmarks: List[Landmark] = field(default_factory=list)
    motion: MotionState = field(default_factory=MotionState)
    metadata: Dict[str, float] = field(default_factory=dict)


@dataclass
class GestureEvent:
    name: str
    confidence: float
    timestamp: float
    details: Optional[Dict[str, float]] = None
