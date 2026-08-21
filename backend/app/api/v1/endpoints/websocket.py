from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core.security import decode_token
from app.websockets.connection_manager import connection_manager

router = APIRouter(tags=["WebSocket"])


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str):
    payload = decode_token(token)
    if payload is None:
        await websocket.close(code=4001)
        return

    user_id = payload.sub
    await connection_manager.connect(user_id, websocket)
    try:
        while True:
            await websocket.receive_text()  # heartbeat / keepalive from client
    except WebSocketDisconnect:
        connection_manager.disconnect(user_id, websocket)
