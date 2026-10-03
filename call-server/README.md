# Wisp Call - server

Signaling server (FastAPI + WebSocket) and TURN relay (coturn), both in Docker. The call page itself is `call.html` in the repository root.

## Run

1. Create the secret (never commit it):
   ```
   echo "TURN_SECRET=$(openssl rand -hex 24)" > .env
   ```
2. In `turnserver.conf` set `external-ip` and `realm` to your own server.
3. Start:
   ```
   docker compose up -d --build
   ```
4. nginx: proxy `/call/ws/` and `/call/api/` to `127.0.0.1:8066` - see `wispplayer.nginx` as an example.

Open ports: `3478` (UDP/TCP) and `49160-49200` (UDP) for audio relay.

The signaling server keeps nothing: rooms live in memory, audio never touches it. TURN passwords are temporary (12 h) and are generated from `TURN_SECRET`.
