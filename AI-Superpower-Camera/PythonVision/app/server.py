from __future__ import annotations

import argparse
import asyncio
import json
import time
from typing import Any, Dict, List, Optional, Set

import websockets
from websockets.server import WebSocketServerProtocol

from .config_loader import load_config
from .custom_power_generator import generate_power_profile
from .gesture_ml import GestureMLClassifier, MLClassifierConfig
from .gesture_rules import classify_rule_based
from .power_engine import PowerEngine
from .storage import PowerStore
from .types import GestureEvent
from .vision import VisionPipeline


class SuperpowerServer:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.clients: Set[WebSocketServerProtocol] = set()
        self.vision = VisionPipeline(config)
        self.ml_classifier = GestureMLClassifier(
            MLClassifierConfig(
                mode=config["ml"]["classifier_mode"],
                tflite_model_path=config["ml"]["tflite_model_path"],
                onnx_model_path=config["ml"]["onnx_model_path"],
            )
        )
        self.power_engine = PowerEngine(config)
        self.store = PowerStore(config["app"]["sqlite_path"])

    async def register(self, websocket: WebSocketServerProtocol) -> None:
        self.clients.add(websocket)
        await websocket.send(json.dumps({"type": "connected", "ts": time.time()}))

    async def unregister(self, websocket: WebSocketServerProtocol) -> None:
        self.clients.discard(websocket)

    async def broadcast(self, payload: Dict[str, Any]) -> None:
        if not self.clients:
            return
        data = json.dumps(payload)
        await asyncio.gather(*[client.send(data) for client in list(self.clients)], return_exceptions=True)

    async def process_client_msg(self, websocket: WebSocketServerProtocol, msg: str) -> None:
        data = json.loads(msg)
        msg_type = data.get("type")

        if msg_type == "create_custom_power":
            power = {
                "name": data["name"],
                "primary_color": data["primary_color"],
                "secondary_color": data["secondary_color"],
                "particle_profile": data["particle_profile"],
                "sound_profile": data["sound_profile"],
            }
            self.store.upsert_power(power)
            await websocket.send(json.dumps({"type": "custom_power_saved", "power": power}))

        elif msg_type == "generate_custom_power":
            name = str(data["name"]).strip()
            power = generate_power_profile(name)
            self.store.upsert_power(power)
            await websocket.send(json.dumps({"type": "custom_power_generated", "power": power}))

        elif msg_type == "list_custom_powers":
            powers = self.store.list_powers()
            await websocket.send(json.dumps({"type": "custom_powers", "powers": powers}))

    async def handler(self, websocket: WebSocketServerProtocol):
        await self.register(websocket)
        try:
            async for message in websocket:
                await self.process_client_msg(websocket, message)
        finally:
            await self.unregister(websocket)

    async def vision_loop(self) -> None:
        target_fps = self.config["app"]["target_fps"]
        frame_interval = 1.0 / max(target_fps, 1)

        while True:
            start = time.time()
            frame = self.vision.read_frame()
            if frame is None:
                await asyncio.sleep(frame_interval)
                continue

            events: List[GestureEvent] = []
            events.extend(classify_rule_based(frame))
            events.extend(self.ml_classifier.classify(frame))

            unique = {}
            for evt in events:
                unique[evt.name] = evt

            for evt in unique.values():
                power_msg = self.power_engine.trigger(evt)
                if power_msg:
                    await self.broadcast(power_msg)

            elapsed = time.time() - start
            await asyncio.sleep(max(0.0, frame_interval - elapsed))

    async def run(self) -> None:
        host = self.config["app"]["websocket_host"]
        port = self.config["app"]["websocket_port"]

        async with websockets.serve(self.handler, host, port, max_queue=256, ping_interval=10):
            await self.vision_loop()

    def close(self) -> None:
        self.vision.close()
        self.store.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Superpower Camera Vision Server")
    parser.add_argument("--config", default="config/default.yaml", help="Path to YAML config")
    args = parser.parse_args()

    config = load_config(args.config)
    server = SuperpowerServer(config)

    try:
        asyncio.run(server.run())
    finally:
        server.close()


if __name__ == "__main__":
    main()
