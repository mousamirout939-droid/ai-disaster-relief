"""
In-memory WebSocket connection registry for real-time features (incident
alerts, shelter capacity updates, admin broadcasts). For multi-instance
horizontal scaling, this is backed by a Redis pub/sub fan-out so a message
published on one pod reaches clients connected to any pod.
"""
import asyncio
import json
import logging

from fastapi import WebSocket

from app.core.redis_client import redis_client

logger = logging.getLogger("app.websockets")

REDIS_CHANNEL = "ws:broadcast"


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, set[WebSocket]] = {}
        self._pubsub_task: asyncio.Task | None = None

    async def connect(self, user_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.setdefault(user_id, set()).add(websocket)
        logger.info("WebSocket connected: user=%s total_conns=%d", user_id, len(self.active_connections))

    def disconnect(self, user_id: str, websocket: WebSocket) -> None:
        conns = self.active_connections.get(user_id)
        if conns and websocket in conns:
            conns.remove(websocket)
            if not conns:
                del self.active_connections[user_id]

    async def send_to_user(self, user_id: str, payload: dict) -> None:
        # Publish via Redis so all pods relay to their locally-connected sockets
        await redis_client.publish(REDIS_CHANNEL, json.dumps({"target": user_id, "payload": payload}))

    async def broadcast(self, payload: dict) -> None:
        await redis_client.publish(REDIS_CHANNEL, json.dumps({"target": "*", "payload": payload}))

    async def _deliver_local(self, user_id: str, payload: dict) -> None:
        if user_id == "*":
            targets = [ws for conns in self.active_connections.values() for ws in conns]
        else:
            targets = list(self.active_connections.get(user_id, []))
        for ws in targets:
            try:
                await ws.send_json(payload)
            except Exception:  # noqa: BLE001 -- any send failure means drop the connection
                logger.warning("Failed to deliver websocket message, dropping connection.")

    async def start_redis_listener(self) -> None:
        pubsub = redis_client.pubsub()
        await pubsub.subscribe(REDIS_CHANNEL)
        async for message in pubsub.listen():
            if message["type"] != "message":
                continue
            data = json.loads(message["data"])
            await self._deliver_local(data["target"], data["payload"])


connection_manager = ConnectionManager()