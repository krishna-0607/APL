from __future__ import annotations

from typing import List

from .types import FrameData, GestureEvent, Landmark


def _dist(a: Landmark, b: Landmark) -> float:
    return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2) ** 0.5


def _is_fist(hand: List[Landmark]) -> bool:
    if len(hand) < 21:
        return False
    wrist = hand[0]
    fingertip_ids = [8, 12, 16, 20]
    return all(_dist(hand[i], wrist) < 0.12 for i in fingertip_ids)


def _is_open_palm(hand: List[Landmark]) -> bool:
    if len(hand) < 21:
        return False
    wrist = hand[0]
    fingertip_ids = [8, 12, 16, 20]
    return all(_dist(hand[i], wrist) > 0.20 for i in fingertip_ids)


def _is_index_extended(hand: List[Landmark]) -> bool:
    if len(hand) < 21:
        return False
    wrist = hand[0]
    return _dist(hand[8], wrist) > 0.25 and _dist(hand[12], wrist) < 0.18


def classify_rule_based(frame: FrameData) -> List[GestureEvent]:
    events: List[GestureEvent] = []

    rh = frame.right_hand_landmarks
    lh = frame.left_hand_landmarks

    if _is_fist(rh) and frame.motion.velocity[2] < -0.4:
        events.append(GestureEvent(name="Fireball", confidence=0.85, timestamp=frame.timestamp))

    if _is_index_extended(rh):
        events.append(GestureEvent(name="Lightning", confidence=0.80, timestamp=frame.timestamp))

    if _is_open_palm(rh):
        events.append(GestureEvent(name="Shield", confidence=0.82, timestamp=frame.timestamp))

    if _is_open_palm(rh) and _is_open_palm(lh):
        palms_distance = _dist(rh[0], lh[0]) if len(rh) >= 1 and len(lh) >= 1 else 999.0
        if palms_distance < 0.15:
            events.append(GestureEvent(name="EnergyBlast", confidence=0.84, timestamp=frame.timestamp))

    if len(frame.pose_landmarks) > 16:
        left_wrist = frame.pose_landmarks[15]
        right_wrist = frame.pose_landmarks[16]
        if _dist(left_wrist, right_wrist) < 0.08:
            events.append(GestureEvent(name="Teleport", confidence=0.78, timestamp=frame.timestamp))

    if frame.motion.acceleration[1] < -1.2:
        events.append(GestureEvent(name="Shockwave", confidence=0.76, timestamp=frame.timestamp))

    return events
