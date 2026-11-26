# Device API

A small modular FastAPI service for registering and managing network devices. Routes handle HTTP requests, the service layer applies device rules, the repository keeps data in memory, and the events module creates alerts when a device goes offline.

Device and alert data is stored only in process memory and shared across requests. Restarting the server clears both collections. No database is required.

## Setup

From the project root, create and activate a virtual environment, then install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run

Start the development server from the project root:

```bash
uvicorn app.main:app --reload
```

Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the interactive Swagger UI. The generated OpenAPI document is at [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json).

## Endpoints

- `POST /devices` registers a device and returns `201`.
- `GET /devices` lists registered devices.
- `GET /devices/{device_id}` retrieves a device.
- `PATCH /devices/{device_id}/status` updates a device to `online` or `offline`.
- `GET /alerts` lists offline alerts. An alert is created when an existing device changes from `online` to `offline`.
- `GET /health` returns `{"status":"ok"}`.

Device types are `router`, `switch`, or `server`; IP addresses must be IPv4. Status defaults to `online` when omitted during registration.

## Tests

Run the service tests from the project root:

```bash
python -m pytest -q
```
