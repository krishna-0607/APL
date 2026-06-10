import unittest

from app.gesture_rules import classify_rule_based
from app.types import FrameData, Landmark, MotionState


def hand_open():
    hand = [Landmark(0.0, 0.0, 0.0)]
    hand.extend([Landmark(0.0, 0.0, 0.0) for _ in range(20)])
    for idx in [8, 12, 16, 20]:
        hand[idx] = Landmark(0.5, 0.5, 0.0)
    return hand


def hand_fist():
    hand = [Landmark(0.0, 0.0, 0.0)]
    hand.extend([Landmark(0.0, 0.0, 0.0) for _ in range(20)])
    for idx in [8, 12, 16, 20]:
        hand[idx] = Landmark(0.01, 0.01, 0.0)
    return hand


class GestureRuleTests(unittest.TestCase):
    def test_detect_shield(self):
        frame = FrameData(
            timestamp=1.0,
            right_hand_landmarks=hand_open(),
            motion=MotionState(),
        )
        names = [e.name for e in classify_rule_based(frame)]
        self.assertIn("Shield", names)

    def test_detect_fireball(self):
        frame = FrameData(
            timestamp=1.0,
            right_hand_landmarks=hand_fist(),
            motion=MotionState(velocity=(0.0, 0.0, -0.6)),
        )
        names = [e.name for e in classify_rule_based(frame)]
        self.assertIn("Fireball", names)


if __name__ == "__main__":
    unittest.main()
