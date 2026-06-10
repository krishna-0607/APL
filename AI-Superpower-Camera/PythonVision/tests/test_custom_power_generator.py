import unittest

from app.custom_power_generator import generate_power_profile


class CustomPowerGeneratorTests(unittest.TestCase):
    def test_generate_dragon_flame_profile(self):
        profile = generate_power_profile("Dragon Flame")
        self.assertEqual(profile["name"], "Dragon Flame")
        self.assertIn("primary_color", profile)
        self.assertIn("secondary_color", profile)
        self.assertIn("particle_profile", profile)
        self.assertIn("sound_profile", profile)

    def test_stable_output(self):
        p1 = generate_power_profile("Dragon Flame")
        p2 = generate_power_profile("Dragon Flame")
        self.assertEqual(p1, p2)


if __name__ == "__main__":
    unittest.main()
