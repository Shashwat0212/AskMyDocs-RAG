# Epic 1 — Local Foundations

Tickets: `RAG-001`–`RAG-004`

Runtime: Local

Status: In progress

## Goal

Make FastAPI, Qdrant, Ollama, and common local operations understandable and repeatable before product features begin.

## Tickets

### `RAG-001` — FastAPI Tutorial And Backend Sandbox

Status: implementation and local validation complete; tracking synchronization pending.

- Build a minimal FastAPI application and health endpoint.
- Demonstrate settings, logging, routing, API documentation, and tests.
- Keep ingestion and RAG behavior out of scope.

### `RAG-002` — Docker Compose And Qdrant Local Sandbox

Status: in progress on `feature/shashwat/RAG-002-qdrant-sandbox`.

- Run a pinned Qdrant image through Docker Compose.
- Verify readiness, persistence, collection creation, upsert, search, and deletion.
- Document start, stop, logs, health, and destructive reset commands.
- Keep backend Qdrant integration out of scope.

### `RAG-003` — Ollama Local Model Sandbox

Status: planned and provisional until Jira confirms the key.

- Verify the Ollama service and approved model locally.
- Exercise CLI and HTTP generation.
- Document setup and common failures.
- Keep the product generation client out of scope.

### `RAG-004` — Local Commands And Operations

Status: planned and provisional until Jira confirms the key.

- Consolidate backend, Qdrant, and Ollama commands.
- Document prerequisite checks and troubleshooting.
- Clearly label destructive operations.

## Completion Criteria

- FastAPI health tests pass.
- Qdrant and Ollama can be started and checked independently.
- Normal Qdrant shutdown preserves data.
- Common operations and failures are documented.
- No document-ingestion or RAG product behavior is added.
