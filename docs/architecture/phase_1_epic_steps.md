# Phase 1 Epic Step Plan

## Purpose

This document expands the Phase 1 epic plan into the step-by-step work discussed for Epics 1 through 6. It is a planning artifact, not implementation code.

Epics 1 through 6 deliver the lean MVP. Epics 7 through 9 in `phase_1_core_rag_mvp.md` are post-MVP enhancement epics.

## Epic 1: Backend Foundations And Local Tooling

Outcome: the local backend environment is ready, testable, observable, and understandable before RAG feature work starts.

### Step 1: Minimal FastAPI Backend Skeleton

Build a tiny FastAPI backend with a health endpoint.

Expected shape:

```text
backend/
  app/
    main.py
    api/routes/health.py
    core/
    schemas/
  tests/
    test_health.py
```

Key behavior:

- `GET /api/v1/health` returns a stable JSON response.
- The app is created through a `create_app()` function so tests can instantiate it cleanly.
- FastAPI auto-docs are available locally.

Out of scope:

- Document upload.
- Qdrant.
- Ollama.
- Retrieval or generation.

### Step 2: Backend Settings

Add typed settings so runtime behavior is not hardcoded.

Settings should cover:

- `APP_ENV`
- `LOG_LEVEL`
- `QDRANT_URL`
- `OLLAMA_BASE_URL`
- model and config file paths

Design direction:

- Use a central settings object.
- Load values from environment/defaults.
- Store settings on app state or inject them into services.
- Add tests for defaults and overrides.

### Step 3: Flow-Level Observability Foundation

Add logging, tracing, and measurement direction early.

Accepted direction:

- One user-initiated workflow gets one `trace_id`.
- The same `trace_id` follows the complete backend flow.
- Internal services accept and propagate a trace context.
- Logs and spans include the same `trace_id`.
- OpenTelemetry, Prometheus, and Grafana OSS are the preferred local-first observability stack.
- VizTracer can be used as optional local developer profiling.

Example flow:

```text
ask question
  -> embed query
  -> dense retrieval
  -> lexical retrieval
  -> fusion
  -> prompt assembly
  -> Ollama generation
  -> citation mapping
  -> response

same trace_id across all steps
```

Out of scope:

- Paid or hosted observability.
- Grafana Cloud.
- Managed Prometheus.
- Always-on heavy profiling.

### Step 4: Qdrant Local Sandbox

Verify Qdrant locally before backend integration.

Work:

- Add or document local Qdrant startup through Docker Compose.
- Verify health/readiness.
- Understand collections, vector size, distance metric, payloads, upsert, and search.

Important rule:

- The Qdrant collection vector size must match the configured embedding model output.

Out of scope:

- Backend indexing.
- Backend retrieval.
- Production deployment.

### Step 5: Ollama Local Sandbox

Verify Ollama locally before backend generation integration.

Work:

- Verify Ollama is reachable on `localhost:11434`.
- Pull or run an approved local model.
- Test CLI generation and HTTP API generation.
- Document expected model names from config.

Out of scope:

- Backend Ollama client.
- Prompt templates.
- Answer API.

### Step 6: Local Commands And Operations Workflow

Make local workflows repeatable.

Expected command coverage:

- backend tests
- backend dev server
- Qdrant start/stop/check
- Ollama check
- optional observability startup/check later

Docs should explain the underlying commands, not only the shortcut names.

## Epic 2: Document Ingestion Pipeline

Outcome: documents can enter the system and become clean, metadata-rich chunks.

### Step 1: Upload API

Add a document upload endpoint.

Expected shape:

```text
POST /api/v1/documents
```

The endpoint accepts a supported file and returns document ingestion metadata such as `document_id`, status, and chunk count.

### Step 2: File Validation

Validate supported file types and reject unsupported inputs clearly.

Initial supported types should stay narrow for the MVP, such as:

- PDF
- TXT
- Markdown

Validation should avoid feature creep into advanced parsing.

### Step 3: Local Storage Boundary

Define how uploaded files are handled locally.

Direction:

- Keep storage local-first.
- Avoid cloud storage.
- Separate raw upload handling from extraction/chunking logic.
- Preserve enough source metadata for citations.

### Step 4: Text Extraction

Extract readable text from supported files.

Expected outputs:

- extracted text
- source metadata
- page or section metadata where available

### Step 5: Pluggable Chunking

Chunking is a tunable RAG hyperparameter and must not be one hardcoded function.

Design direction:

- A main chunking module owns the common interface and orchestration.
- Individual strategies live in separate modules.
- Strategy selection and parameters are configuration-driven.
- The ingestion pipeline depends on the chunking interface, not a specific implementation.

Example future strategies:

- fixed-size chunking
- recursive text chunking
- Markdown heading-aware chunking
- PDF page-aware chunking
- hybrid or staged chunking

Example config shape:

```yaml
chunking:
  strategy: recursive_text
  chunk_size: 800
  chunk_overlap: 100
```

### Step 6: Metadata And Tests

Create chunk records with stable metadata.

Chunk records should preserve:

- `document_id`
- `chunk_id`
- source name
- chunk index
- page or section when available
- text

Tests should cover file validation, extraction, chunking, and metadata.

## Epic 3: Embedding And Vector Indexing

Outcome: chunks are stored canonically and indexed for dense and future lexical retrieval.

### Step 1: Embedding Interface

Create an embedding client boundary.

Direction:

- Start with local embedding execution only.
- Keep model name and dimensions configurable.
- Return vectors with enough metadata to validate compatibility with Qdrant.

Out of scope:

- Hosted embedding APIs.
- Paid embedding services.

### Step 2: Canonical Chunk Store

Persist the complete chunk text and metadata in a local canonical store.

Direction:

- SQLite is the expected local store for chunk records.
- The canonical store owns full text and stable metadata.
- Qdrant and lexical search indexes should be rebuildable from the canonical store.

Important boundary:

```text
canonical chunk store != vector index payload
canonical chunk store != lexical search index
```

### Step 3: Qdrant Vector Index

Index chunk embeddings in Qdrant.

Direction:

- Store vectors in Qdrant.
- Store lightweight payload metadata needed for filtering and result lookup.
- Do not rely on Qdrant as the only source of full chunk text.

### Step 4: SQLite FTS Preparation

Prepare local lexical search over the same canonical chunk text.

Direction:

- Use SQLite FTS5 for MVP lexical search unless later implementation constraints force a different local option.
- Keep lexical indexing separate from Qdrant.
- Use canonical chunk IDs to join dense and lexical results later.

### Step 5: Indexing Flow

Connect ingestion output to storage and indexing.

Flow:

```text
chunks
  -> canonical chunk store
  -> embedding model
  -> Qdrant vector index
  -> SQLite FTS lexical index
```

### Step 6: Indexing Tests

Tests should cover:

- embeddings generated for chunks
- vector dimension validation
- canonical chunk persistence
- Qdrant upsert call behavior
- SQLite FTS record creation
- rebuildability from canonical records

## Epic 4: Hybrid Retrieval Pipeline

Outcome: the backend can retrieve relevant chunks using dense and lexical retrieval, then fuse the results.

### Step 1: Retrieval API Shape

Define a retrieval service interface before wiring answer generation.

Expected input:

- query text
- filters
- retrieval config
- trace context

Expected output:

- ranked hydrated chunks
- scores and score components where useful
- source metadata for citation mapping

### Step 2: Dense Retrieval

Query Qdrant for semantic matches.

Behavior:

- Embed the query.
- Search Qdrant.
- Return chunk IDs, scores, and metadata.
- Keep top-k configurable.

### Step 3: Lexical Retrieval

Query the local lexical index for keyword/BM25-style matches.

Direction:

- Use SQLite FTS5/BM25 for local-first lexical retrieval.
- Search over canonical chunk text.
- Return chunk IDs, lexical scores, and metadata.

### Step 4: Fusion

Combine dense and lexical results into one ranked list.

Direction:

- Keep the fusion method configurable.
- Start with a simple, explainable fusion approach such as reciprocal rank fusion.
- Preserve per-source scores for debugging and evaluation.

Example config shape:

```yaml
retrieval:
  dense_top_k: 10
  lexical_top_k: 10
  fusion: reciprocal_rank
```

### Step 5: Hydration

Fetch full chunk text and citation metadata from the canonical store after ranking.

Important boundary:

- Retrieval can rank by IDs and scores.
- Answer generation needs hydrated text and citation metadata.

### Step 6: Reranking Placeholder

Reserve config shape for reranking, but keep it disabled and out of scope for the MVP retrieval epic.

Expected reserved config:

```yaml
retrieval:
  reranking:
    enabled: false
    provider: local_cross_encoder
    model: cross-encoder/ms-marco-MiniLM-L-6-v2
    top_n_input: 20
    top_k_output: 5
```

Reranking implementation belongs to Epic 7.

### Step 7: Retrieval Tests

Tests should cover:

- dense-only retrieval behavior
- lexical-only retrieval behavior
- hybrid fusion ordering
- hydration by chunk ID
- config-controlled top-k values
- reranking disabled behavior

## Epic 5: Answer Generation With Citations

Outcome: the backend can answer a question from retrieved chunks and return citation metadata.

### Step 1: Prompt Template Design

Generate prompts through templates, not ad hoc strings scattered through services.

Direction:

- Store prompt templates in a dedicated module or config-managed location.
- Separate system instructions, question, retrieved context, and output format.
- Keep room for session context to be added later without rewriting prompt assembly.

### Step 2: Prompt Assembly Service

Build a service that takes retrieved chunks and returns a final prompt.

Inputs:

- user question
- hydrated chunks
- citation labels
- optional future session context
- trace context

Output:

- prompt text or structured prompt payload for the generation client

### Step 3: Ollama Generation Client

Call Ollama through a local generation client.

Direction:

- Base URL, model, timeout, and generation settings come from config.
- The client handles local connection errors clearly.
- No hosted LLM API is introduced.

### Step 4: Citation Mapping

Map generated answers back to retrieved sources.

Direction:

- Use stable citation labels generated from retrieved chunks.
- Return citation metadata even when the answer text is short.
- Preserve document name, page or section, and chunk ID where available.

### Step 5: Answer API

Expose a document-grounded ask endpoint.

Expected shape:

```text
POST /api/v1/answers
```

Expected response:

- answer text
- citations
- trace ID
- retrieval metadata useful for debugging

### Step 6: Minimal Session Behavior

The MVP answer flow should be stateless or only minimally session-aware.

Out of scope:

- Long-term conversation memory.
- Session memory indexes.
- Conversation summarization.

Session memory belongs to Epic 8.

### Step 7: Generation Tests

Tests should cover:

- prompt assembly with citations
- Ollama client success and failure behavior through test doubles
- answer response shape
- no-answer or insufficient-context behavior
- trace ID propagation through the answer flow

## Epic 6: MVP Gradio Interface

Outcome: a local UI can upload a document, ask a question, and display an answer with citations.

### Step 1: Gradio App Skeleton

Create a minimal local Gradio app that can call the backend API.

Direction:

- Keep it thin.
- Avoid duplicating backend logic in the UI.
- Use backend endpoints as the source of behavior.

### Step 2: Upload Flow

Add a document upload control.

Behavior:

- Select a supported file.
- Send it to the backend upload endpoint.
- Show ingestion status and basic metadata.

### Step 3: Question Flow

Add a question input and submit action.

Behavior:

- Send the question to the backend answer endpoint.
- Show loading state while the backend works.
- Display backend errors clearly.

### Step 4: Answer And Citations Display

Show the generated answer and supporting citations.

Direction:

- Citations should be visible enough to validate grounding.
- Include source name and page or section when available.
- Keep debug metadata available without overwhelming the MVP UI.

### Step 5: Basic Error And Empty States

Handle common local failures:

- backend not running
- unsupported file
- no document uploaded
- Ollama unavailable
- no relevant chunks found

### Step 6: MVP Run Workflow

Document how to run the complete local MVP.

Expected workflow:

```text
start local services
start backend
start Gradio
upload document
ask question
inspect answer and citations
```

### Step 7: UI Smoke Tests

Tests or manual verification should cover:

- app starts locally
- upload control reaches backend
- question flow reaches backend
- answer and citations render
- basic error states are visible
