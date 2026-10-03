import base64
import hashlib
import hmac
import json
import os
import secrets
import time

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

# room -> {peer_id: websocket}
rooms: dict[str, dict[str, WebSocket]] = {}
MAX_PEERS = 4

TURN_SECRET = os.environ.get("TURN_SECRET", "")
TURN_HOST = "wispplayer.com"
TURN_TTL = 12 * 3600


async def safe_send(ws: WebSocket, msg: dict) -> None:
    try:
        await ws.send_text(json.dumps(msg))
    except Exception:
        pass


@app.get("/call/api/health")
def health():
    return {"ok": True, "rooms": len(rooms), "peers": sum(len(p) for p in rooms.values())}


@app.get("/call/api/turn")
def turn():
    # временный логин/пароль для coturn (схема use-auth-secret)
    if not TURN_SECRET:
        return {"iceServers": []}
    user = f"{int(time.time()) + TURN_TTL}:wisp"
    cred = base64.b64encode(hmac.new(TURN_SECRET.encode(), user.encode(), hashlib.sha1).digest()).decode()
    return {"iceServers": [{
        "urls": [f"turn:{TURN_HOST}:3478?transport=udp", f"turn:{TURN_HOST}:3478?transport=tcp"],
        "username": user,
        "credential": cred,
    }]}


@app.websocket("/call/ws/{room}")
async def ws_room(websocket: WebSocket, room: str):
    await websocket.accept()

    clean = room.replace("-", "").replace("_", "")
    if not room or len(room) > 64 or not clean.isalnum():
        await safe_send(websocket, {"type": "error", "reason": "bad_room"})
        await websocket.close(code=4400)
        return

    peers = rooms.setdefault(room, {})
    if len(peers) >= MAX_PEERS:
        await safe_send(websocket, {"type": "full"})
        await websocket.close(code=4403)
        return

    pid = secrets.token_hex(4)
    # new peer learns who is already here; others learn about the new peer
    await safe_send(websocket, {"type": "welcome", "id": pid, "peers": list(peers)})
    for other in list(peers.values()):
        await safe_send(other, {"type": "join", "id": pid})
    peers[pid] = websocket

    try:
        while True:
            raw = await websocket.receive_text()
            if len(raw) > 65536:
                continue
            try:
                msg = json.loads(raw)
            except ValueError:
                continue
            if not isinstance(msg, dict):
                continue
            to = msg.get("to")
            if to and to in peers:
                msg["from"] = pid
                await safe_send(peers[to], msg)
            # messages without "to" (e.g. ping) just keep the connection alive
    except WebSocketDisconnect:
        pass
    finally:
        peers.pop(pid, None)
        for other in list(peers.values()):
            await safe_send(other, {"type": "leave", "id": pid})
        if not peers:
            rooms.pop(room, None)
