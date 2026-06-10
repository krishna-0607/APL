import asyncio
import json
import tempfile
import unittest

try:
    import websockets
except Exception:  # pragma: no cover
    websockets = None

if websockets is not None:
    from app.server import SuperpowerServer


@unittest.skipIf(websockets is None, "websockets dependency is not installed")
class WebSocketIntegrationTests(unittest.IsolatedAsyncioTestCase):
    async def test_custom_power_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            config = {
                "app": {
                    "websocket_host": "127.0.0.1",
                    "websocket_port": 8877,
                    "target_fps": 1,
                    "camera_index": 0,
                    "sqlite_path": f"{d}/powers.db",
                },
                "vision": {"min_detection_confidence": 0.5, "min_tracking_confidence": 0.5},
                "ml": {"classifier_mode": "none", "tflite_model_path": "", "onnx_model_path": ""},
                "power": {
                    "fireball_cooldown_s": 1,
                    "lightning_cooldown_s": 1,
                    "shield_cooldown_s": 1,
                    "energy_blast_cooldown_s": 1,
                    "teleport_cooldown_s": 1,
                    "shockwave_cooldown_s": 1,
                },
            }
            server = SuperpowerServer(config)

            async def run_server():
                async with websockets.serve(server.handler, "127.0.0.1", 8877):
                    await asyncio.sleep(0.5)

            server_task = asyncio.create_task(run_server())
            await asyncio.sleep(0.1)

            async with websockets.connect("ws://127.0.0.1:8877") as ws:
                await ws.recv()  # connected
                await ws.send(
                    json.dumps(
                        {
                            "type": "create_custom_power",
                            "name": "Dragon Flame",
                            "primary_color": "#FF5500",
                            "secondary_color": "#FFD000",
                            "particle_profile": "fire_trail",
                            "sound_profile": "dragon_roar",
                        }
                    )
                )
                response = json.loads(await ws.recv())
                self.assertEqual(response["type"], "custom_power_saved")

            server_task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await server_task
            server.close()


if __name__ == "__main__":
    unittest.main()
