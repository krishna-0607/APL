import tempfile
import unittest

from app.storage import PowerStore


class StoreTests(unittest.TestCase):
    def test_upsert_and_list(self):
        with tempfile.TemporaryDirectory() as d:
            store = PowerStore(f"{d}/powers.db")
            store.upsert_power(
                {
                    "name": "Dragon Flame",
                    "primary_color": "#FF5500",
                    "secondary_color": "#FFD000",
                    "particle_profile": "fire_trail",
                    "sound_profile": "dragon_roar",
                }
            )
            powers = store.list_powers()
            self.assertEqual(len(powers), 1)
            self.assertEqual(powers[0]["name"], "Dragon Flame")
            store.close()


if __name__ == "__main__":
    unittest.main()
