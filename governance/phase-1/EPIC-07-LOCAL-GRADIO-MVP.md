# Epic 7 — Local Gradio MVP

Tickets: `RAG-042`–`RAG-047`

Runtime: Local FastAPI, Docker Qdrant, Ollama, and Gradio

Status: Planned

## Goal

Rebuild the selected profiles locally and deliver the complete upload-to-cited-answer workflow through a thin Gradio interface.

## Tickets

- `RAG-042`: rehydrate and validate the Epic 5 profiles on the local runtime.
- `RAG-043`: thin Gradio application shell that calls FastAPI.
- `RAG-044`: document upload, validation, ingestion progress, and result states.
- `RAG-045`: question-and-answer flow using the query navigator.
- `RAG-046`: citations, profile provenance, loading, empty, insufficient-context, and error states.
- `RAG-047`: end-to-end smoke tests and local operating guide.

## Completion Criteria

- Selected profiles rebuild locally and pass compatibility checks.
- Gradio does not duplicate backend business logic.
- The local flow uploads, extracts, chunks, indexes, scans, selects profiles, retrieves, reranks, generates, and displays citations.
- The UI clearly shows loading, validation, empty, insufficient-context, and service failure states.
- The end-to-end smoke test and operating instructions pass on the supported local environment.

Phase 1 is complete when this epic is validated and merged into `main`.
