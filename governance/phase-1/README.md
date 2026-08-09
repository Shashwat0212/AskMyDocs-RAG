# Phase 1 — Core RAG MVP

## Goal

Deliver a local application that uploads supported documents, builds a Qdrant hybrid index, retrieves and reranks evidence using benchmark-selected profiles, generates an Ollama answer, and displays citations in Gradio.

## Sequence

| Epic | Tickets | Canonical runtime |
|---|---|---|
| [1 — Local Foundations](EPIC-01-LOCAL-FOUNDATIONS.md) | `RAG-001`–`RAG-004` | Local |
| [2 — Document Ingestion](EPIC-02-INGESTION.md) | `RAG-005`–`RAG-010` | Colab |
| [3 — Indexing and Retrieval](EPIC-03-INDEXING-AND-RETRIEVAL.md) | `RAG-011`–`RAG-021` | Colab |
| [4 — Retrieval Evaluation](EPIC-04-RETRIEVAL-EVALUATION.md) | `RAG-022`–`RAG-028` | Colab |
| [5 — Profiles and Navigator](EPIC-05-PROFILES-AND-NAVIGATOR.md) | `RAG-029`–`RAG-037` | Colab |
| [6 — Answer Generation](EPIC-06-GENERATION.md) | `RAG-038`–`RAG-041` | Colab |
| [7 — Local Gradio MVP](EPIC-07-LOCAL-GRADIO-MVP.md) | `RAG-042`–`RAG-047` | Local |

Ticket references not confirmed in Jira are provisional planning identifiers.

## Runtime And Storage

- Epic 1 uses local FastAPI, Docker Qdrant, Ollama, and local volumes.
- Epics 2–6 use pinned free-tier Colab environments with self-managed Qdrant and Ollama processes.
- Colab Qdrant data stays on the runtime filesystem and is disposable.
- Shared Drive stores declared datasets, checkpoints, and full experiment artifacts.
- Git stores reviewed code, compact fixtures, profiles, manifests, and summaries.
- Epic 7 rebuilds the selected profiles on the local runtime.

## Phase 1 Boundaries

- Qdrant owns dense vectors, sparse/BM25 vectors, fusion, filters, chunk payloads, and citation metadata.
- SQLite is not part of the Phase 1 document path.
- Retrieval quality is measured before answer generation.
- Generation tests integration, citations, provenance, and failures; it does not attempt broad model ranking.
- No paid API, hosted vector database, paid evaluation, or paid observability service is allowed.
- Session memory, semantic cache, model routing, arbitration, final React UI, and full answer-quality evaluation remain post-MVP.

## Shared Contracts

An ingestion/index profile controls parser, chunking, embedding, dimensions, and Qdrant collection/index settings. A query profile controls collection-compatible candidate limits, fusion, thresholds, filtering, reranking, and final result count.

Every run records source commit, corpus checksum, profile IDs and hashes, runtime and model versions, metrics, errors, state, and artifact locations. Every answer records its ingestion profile, query profile, trace ID, citations, and fallback state.
