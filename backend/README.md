# Backend

This folder now contains a minimal FastAPI sandbox for local experimentation.

## Current responsibilities

- Provide a simple FastAPI application entrypoint.
- Expose a lightweight `/health` endpoint for local smoke testing.
- Demonstrate environment-based settings and logging without adding monitoring infrastructure.
- Offer a small regression test for the health route.

## Run locally

```bash
cd d:\AskMyDocs-RAG\backend
.\.venv\Scripts\Activate.ps1
python app/main.py
```

## Useful commands

```bash
pytest backend/tests/test_health.py
```

## Notes

- The app exposes a lightweight `/health` endpoint and a simple `/info` endpoint.
- Logging is configured through the Python `logging` module.
- Settings are read from environment variables via `APP_NAME`, `APP_ENV`, and `DEBUG`.
- The implementation intentionally avoids external monitoring services.
