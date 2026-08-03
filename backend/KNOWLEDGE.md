# Backend Knowledge

## Current State

The backend folder now contains a minimal FastAPI sandbox for local experimentation. It includes a lightweight application entrypoint, a health endpoint, environment-driven settings, structured logging, and a regression test for the health route.

## Current Structure

- `app/main.py` – minimal FastAPI application with `/health`, `/`, and `/info` endpoints.
- `tests/test_health.py` – regression test covering the health endpoint.
- `requirements.txt` – local Python dependencies for the sandbox.

## Runtime Notes

- The sandbox is intentionally lightweight and does not introduce observability services or external monitoring.
- Settings are read from environment variables such as `APP_NAME`, `APP_ENV`, and `DEBUG`.
- Local runs should use the project virtual environment and `uvicorn`.

## Update Notes

When backend implementation expands, update this file with the actual module layout, runtime entrypoints, service boundaries, configuration files used, and tests that cover backend behavior.

