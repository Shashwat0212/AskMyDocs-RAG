# FastAPI Fundamentals Learning Lab

This directory is a disposable, local-only learning lab for `RAG-001`. It is
intentionally separate from the future AskMyDocs production backend. Change it,
break it, add routes, and rewrite tests as you learn.

The lab uses only in-memory data. It does not require Docker, Qdrant, Ollama, a
database, credentials, or a hosted service.

## What the lab demonstrates

- A modular FastAPI application and an application factory
- Startup and shutdown behavior through an application lifespan
- Path, query, and JSON body validation
- Pydantic request and response models
- Dependency injection and application state
- Async route handlers and expected HTTP errors
- Request middleware, request IDs, timing, and logging
- Environment-driven settings
- Swagger UI, ReDoc, and OpenAPI
- API tests using pytest and FastAPI's `TestClient`

## Project layout

```text
FASTAPI/
├── app/
│   ├── main.py
│   ├── settings.py
│   ├── store.py
│   ├── dependencies.py
│   ├── middleware.py
│   ├── schemas.py
│   └── routers/
│       ├── health.py
│       └── items.py
├── tests/
├── main.py
├── pyproject.toml
└── uv.lock
```

## Setup

Run all commands from this directory:

```bash
cd backend/FASTAPI
uv sync --python 3.11
```

`uv` creates or updates the ignored `.venv` and installs the locked runtime and
development dependencies.

## Start the server

```bash
uv run uvicorn app.main:app --reload
```

The server listens at `http://127.0.0.1:8000`.

Open these pages in a browser:

- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>
- OpenAPI JSON: <http://127.0.0.1:8000/openapi.json>

## Exercise the API

Check health:

```bash
curl -i http://127.0.0.1:8000/api/v1/health
```

Create two items:

```bash
curl -i -X POST http://127.0.0.1:8000/api/v1/items \
  -H 'Content-Type: application/json' \
  -d '{"name":"FastAPI book","description":"Tutorial notes"}'

curl -i -X POST http://127.0.0.1:8000/api/v1/items \
  -H 'Content-Type: application/json' \
  -d '{"name":"HTTP client"}'
```

List items and practice validated query parameters:

```bash
curl -i 'http://127.0.0.1:8000/api/v1/items?offset=0&limit=10'
```

Fetch, replace an item through `PATCH`, and then delete it:

```bash
curl -i http://127.0.0.1:8000/api/v1/items/1
curl -i -X PATCH http://127.0.0.1:8000/api/v1/items/1 \
  -H 'Content-Type: application/json' \
  -d '{"name":"Updated FastAPI book","description":"Practiced PATCH"}'
curl -i -X DELETE http://127.0.0.1:8000/api/v1/items/1
```

Trigger a request-body validation error (`422`):

```bash
curl -i -X POST http://127.0.0.1:8000/api/v1/items \
  -H 'Content-Type: application/json' \
  -d '{"name":""}'
```

Trigger a missing-resource error (`404`):

```bash
curl -i http://127.0.0.1:8000/api/v1/items/999
```

Supply your own request ID and observe it in the response header and logs:

```bash
curl -i http://127.0.0.1:8000/api/v1/health \
  -H 'X-Request-ID: my-learning-request'
```

The in-memory store resets whenever the server restarts.

## Settings and logging

The defaults are:

| Environment variable | Default |
|---|---|
| `APP_NAME` | `FastAPI Fundamentals Lab` |
| `APP_ENV` | `local` |
| `LOG_LEVEL` | `INFO` |

Override settings for one server run:

```bash
APP_ENV=practice LOG_LEVEL=DEBUG \
  uv run uvicorn app.main:app --reload
```

The app also reads the ignored `.env` in this directory. Never commit secrets or
local `.env` contents.

## Run tests

Run everything:

```bash
uv run pytest -v
```

Run one module or one test:

```bash
uv run pytest -v tests/test_items.py
uv run pytest -v tests/test_items.py::test_invalid_item_is_rejected
```

Useful pytest options:

```bash
uv run pytest -vv
uv run pytest -k health
uv run pytest -x
uv run pytest --collect-only
```

## Suggested experiments

1. Change an expected status code in a test, see it fail, then repair it.
2. Add a maximum `limit` test and change the constraint in
   `app/dependencies.py`.
3. Add a field to `ItemCreate` and inspect how Swagger UI and validation change.
4. Make `PATCH /api/v1/items/{item_id}` accept partial updates by adding a
   dedicated model with optional fields.
5. Replace the default missing-item detail and update the relevant assertions.
6. Send the same `X-Request-ID` on several requests and follow the log lines.
7. Add a dependency that requires a practice header, then override it in a test.
8. Compare a normal `def` route with an `async def` route using the FastAPI docs.

## Resetting the lab

Restarting Uvicorn resets all item data. To restore code after an experiment,
use your editor's undo/history or inspect the branch diff with:

```bash
git diff -- backend/FASTAPI
git status --short backend/FASTAPI
```

## References

- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [FastAPI settings and environment variables](https://fastapi.tiangolo.com/advanced/settings/)
- [uv project dependencies](https://docs.astral.sh/uv/concepts/projects/dependencies/)
