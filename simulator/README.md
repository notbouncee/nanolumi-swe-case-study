# Device Simulator

This directory contains the files required to run the pre-built device simulator.

## Requirements

- Docker
- Docker Compose

## 1. Load the simulator image

```bash
gunzip -c water-quality-simulator-1.0.0.tar.gz | docker load
```

Some Docker installations may support:

```bash
docker load -i water-quality-simulator-1.0.0.tar.gz
```

## 2. Start the simulator

```bash
cp .env.example .env
docker compose up
```

The simulator will be available at:

```text
http://localhost:9000
```

In another terminal, verify that it is running:

```bash
curl http://localhost:9000/health
curl http://localhost:9000/api/devices
```

The health endpoint should return `{"status":"ok"}`. The devices endpoint should return the simulated device list.

Useful endpoints:

- `GET /health`
- `GET /api/devices`
- `POST /api/devices/{device_id}/measurements`

The full communication contract is documented in `../SIMULATOR_PROTOCOL.md`.

## Send a test command

After your application exposes a callback endpoint, you can send a measurement command through your application or directly with `curl`.

Example direct command:

```bash
curl -i -X POST http://localhost:9000/api/devices/device-001/measurements \
  -H 'Content-Type: application/json' \
  -d '{
    "request_id": "req-local-test-001",
    "requested_at": "2026-07-11T03:15:00Z",
    "callback_url": "http://host.docker.internal:8000/api/device-results",
    "parameters": ["ph", "temperature_c"]
  }'
```

Use a callback URL that points to your own backend. The acknowledgement response only confirms that the simulator received the command. The final result is delivered later to your callback endpoint.

## Callback URL

The simulator runs inside Docker. If your application runs directly on the host machine, a callback URL may look like:

```text
http://host.docker.internal:8000/api/device-results
```

Replace the port and path with those used by your application.

If your application also runs in Docker Compose, use the service name and port on the Compose network instead of `host.docker.internal`.

## Common issues

- If the simulator starts but your application never receives callbacks, check that the callback URL is reachable from inside the simulator container.
- If you reuse the same `request_id`, the simulator may treat the command as the same logical request. Generate a new `request_id` for each new operator request.
- If you change simulator environment settings or want a clean database, run `docker compose down -v` before starting it again.
- If Docker reports that port `9000` is already in use, set `SIMULATOR_PORT` in `.env` to another host port, such as `9001`.

## Stop the simulator

```bash
docker compose down
```

To also remove the simulator's local data volume:

```bash
docker compose down -v
```

The simulator represents an independently operated external system. You are not expected to modify or depend on its internal implementation.
