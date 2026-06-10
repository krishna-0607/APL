from __future__ import annotations

import argparse
import asyncio
import json
from dataclasses import dataclass, field
from typing import Dict, Set

import websockets
from websockets.server import WebSocketServerProtocol


@dataclass
class PlayerState:
    hp: float = 100.0
    last_power: str = ""


class MultiplayerRelayServer:
    def __init__(self) -> None:
        self.clients: Set[WebSocketServerProtocol] = set()
        self.states: Dict[str, PlayerState] = {}

    async def register(self, ws: WebSocketServerProtocol) -> None:
        self.clients.add(ws)
        player_id = f"player-{id(ws)}"
        self.states[player_id] = PlayerState()
        await ws.send(json.dumps({"type": "joined", "player_id": player_id, "hp": 100.0}))

    async def unregister(self, ws: WebSocketServerProtocol) -> None:
        self.clients.discard(ws)

    async def broadcast(self, payload: dict) -> None:
        if not self.clients:
            return
        msg = json.dumps(payload)
        await asyncio.gather(*[c.send(msg) for c in list(self.clients)], return_exceptions=True)

    async def handle(self, ws: WebSocketServerProtocol) -> None:
        await self.register(ws)
        try:
            async for msg in ws:
                data = json.loads(msg)
                if data.get("type") == "power_hit":
                    damage = float(data.get("damage", 0.0))
                    power = str(data.get("power", "Unknown"))
                    await self.broadcast(
                        {
                            "type": "damage_event",
                            "power": power,
                            "damage": damage,
                        }
                    )
        finally:
            await self.unregister(ws)


async def main(host: str, port: int) -> None:
    relay = MultiplayerRelayServer()
    async with websockets.serve(relay.handle, host, port, max_queue=256):
        await asyncio.Future()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multiplayer relay server")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=9000)
    args = parser.parse_args()
    asyncio.run(main(args.host, args.port))
