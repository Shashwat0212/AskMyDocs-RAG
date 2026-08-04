# Phase 1 Core RAG MVP Plan

## Purpose

Phase 1 delivers a cited document-question-answering MVP through seven ordered epics. Epic 1 remains local. Epics 2 through 6 use free-tier Google Colab as the canonical shared execution environment. Epic 7 rehydrates the selected configuration on the local Docker/Qdrant/Ollama runtime and completes the Gradio MVP.

Ticket references are sequential from `RAG-001` through `RAG-041`. References not yet created in Jira are provisional until confirmed.

## Runtime And Persistence Model

| Segment | Canonical runtime | Durable records |
|---|---|---|
| Epic 1 | Local FastAPI, Docker Compose, Qdrant, and Ollama | Git and local Docker volumes |
| Epics 2–6 | Free-tier Colab with pinned dependencies and ephemeral self-managed Qdrant/Ollama | Git for reviewed code/config/summaries; shared Drive for datasets and full artifacts |
| Epic 7 | Local FastAPI, Docker Qdrant, Ollama, and Gradio | Git profiles plus local runtime data |

Qdrant storage in Colab must stay under the runtime filesystem, never directly on mounted Drive. Collections may be discarded after a run and must be rebuildable from source documents, dataset manifests, profiles, and run manifests.

## Phase 1 Outcome

At the end of Epic 7, a developer can locally upload a supported document, extract and chunk it, build Qdrant dense and sparse/BM25 indexes, retrieve with native fusion, rerank candidates, generate an Ollama answer, and display citations in Gradio using profiles validated across datasets in Colab.

Phase 1 excludes paid services, hosted vector databases, deployment pipelines, semantic caching, model routing, arbitration, full generation evaluation automation, the final React/Next.js interface, and session memory.

## Configuration Contracts

### Ingestion/Index Profile

Defines parser; chunk strategy, size, and overlap; dense and sparse models; vector dimensions; distance metric; collection naming; HNSW, quantization, optimizer, and payload-index settings; and the complete payload schema.

### Query Profile

Defines dense and sparse prefetch limits, filters, fusion, thresholds, reranker configuration and bounds, fallback behavior, and final output count. Query-time changes must be compatible with the existing collection.

### Run Manifest

Records run ID, source commit, dataset and checksum, runtime details, profile/config hashes, Qdrant and model versions, timestamps, metrics, errors, run state, and artifact locations.

## Epic 1 — Local Backend Foundations

Complete the existing local setup-and-learning epic unchanged before adopting Colab.

Tickets:

- `RAG-001`: FastAPI tutorial and backend sandbox.
- `RAG-002`: Docker Compose and Qdrant local sandbox.
- `RAG-003`: Ollama local model-serving sandbox.
- `RAG-004`: Local backend commands and operations.

Finished state:

- FastAPI skeleton, health endpoint, typed settings, logging, and tests are understood and repeatable.
- Qdrant and Ollama can be started and verified independently on the developer machine.
- Local commands and troubleshooting are documented.

Out of scope: ingestion, embeddings, retrieval, generation, Gradio, and deployment automation.

## Epic 2 — Colab Environment and Document Ingestion

Tickets:

- `RAG-005`: Reproducible Colab bootstrap, branch checkout, dependency installation, shared Drive mounting, and runtime diagnostics.
- `RAG-006`: Document-upload API contract.
- `RAG-007`: File validation and Colab/Drive storage boundary.
- `RAG-008`: PDF, TXT, and Markdown extraction.
- `RAG-009`: Pluggable, configuration-driven chunking.
- `RAG-010`: Stable document/chunk metadata and ingestion tests.

Finished state:

- Any contributor can launch a fresh Colab runtime, check out the assigned branch, install pinned dependencies, mount the configured Drive location, and capture diagnostics.
- Supported documents become stable, citation-aware chunks through importable package code.
- Raw inputs and full artifacts follow the Drive policy while working files remain under the Colab runtime.
- Notebooks are thin launchers, not the only implementation.

## Epic 3 — Qdrant Embedding and Indexing

Tickets:

- `RAG-011`: Dense and sparse embedding interfaces.
- `RAG-012`: Qdrant collection schema with named dense/sparse vectors, complete retrievable chunk payloads, and citation metadata.
- `RAG-013`: Qdrant indexing flow and deterministic collection naming.
- `RAG-014`: Rebuild, compatibility, payload, dimension, and indexing tests.

Finished state:

- Embedding interfaces expose model identity, version, dimensions, and normalization behavior.
- Each Qdrant point contains stable IDs, named dense and sparse/BM25 vectors, full chunk text, source identifiers, chunk order, and page/section citation metadata.
- Collection names identify corpus, profile, and version/run without collisions.
- Source files and dataset manifests remain canonical; ephemeral collections can be rebuilt and compatibility errors fail clearly.

SQLite is not part of the Phase 1 document indexing or retrieval path.

## Epic 4 — Qdrant Hybrid Retrieval and Reranking

Tickets:

- `RAG-015`: Retrieval service/API contract.
- `RAG-016`: Dense Qdrant retrieval.
- `RAG-017`: Qdrant sparse/BM25 retrieval.
- `RAG-018`: Qdrant Query API fusion, with RRF as the initial default and DBSF configurable.
- `RAG-019`: Reranking configuration and interface.
- `RAG-020`: Initial local MiniLM cross-encoder reranker.
- `RAG-021`: Dense, sparse, fusion, payload-hydration, reranking, fallback, and trace tests.

Finished state:

- Qdrant performs named dense and sparse prefetches and native fusion.
- Complete chunks and citation metadata return directly from Qdrant payloads.
- Reranking operates on bounded Qdrant candidates and is configurable, bypassable, and failure-tolerant.
- The initial reranker is `cross-encoder/ms-marco-MiniLM-L-6-v2`.
- Traces preserve dense, sparse, fusion, and reranking provenance.

This epic completes tested retrieval and reranking before any LLM integration.

Reference: [Qdrant hybrid Query API](https://qdrant.tech/documentation/search/hybrid-queries/).

## Epic 5 — Prototype Experimentation and Configuration Navigator

Tickets:

- `RAG-022`: Dataset registry, checksums, query sets, and relevance judgments.
- `RAG-023`: Hyperparameter profile schema and reproducible run manifest.
- `RAG-024`: Create an isolated branch snapshot of the completed Epic 2–4 pipeline and expose plug-in strategy boundaries.
- `RAG-025`: Colab experiment runner supporting configuration matrices, checkpointing, resumption, and failure isolation.
- `RAG-026`: Execute multi-dataset, granular retrieval experiments.
- `RAG-027`: Capture quality, latency, indexing cost, memory, errors, and comparison artifacts.
- `RAG-028`: Produce validated ingestion, index, retrieval, and reranking profiles plus a safe default.
- `RAG-029`: Implement the pre-ingestion scanner, selecting one profile when confident or a resource-capped alternative collection set when uncertain.
- `RAG-030`: Implement the query-time navigator for compatible top-k, thresholds, fusion, filtering, and reranking choices.
- `RAG-031`: Merge validated plug-in architecture, profiles, and navigator contracts into the product pipeline and remove the temporary copied prototype.

Experiment rules:

- The isolated prototype is the Epic 5 integration branch at a recorded commit SHA, not a permanent duplicate codebase.
- Runs are manually launched but automated end to end, checkpointed, resumable, and failure-isolated. They are not unattended Colab schedules.
- Candidate families include parsing/chunking, embedding models and supported dimensions, sparse models, distance metrics, HNSW, optimizer settings, quantization, payload indexes, fusion, thresholds, candidate counts, filters, and reranking.
- Report per-dataset/profile winners and Pareto trade-offs. Do not claim a universal best configuration without evidence.
- Capture retrieval quality such as Recall@k, nDCG@k, MRR@k, or Precision@k where judgments permit, plus indexing duration, query P50/P95, memory, storage, errors, and runtime characteristics.
- Navigator algorithms, confidence thresholds, maximum alternative collections, resource caps, and final parameter values are measured outputs of the epic.

Navigator boundaries:

- The pre-ingestion scanner may choose parsing, chunking, embedding, dimensions, distance, and index settings before collection creation.
- When uncertain, it may create only a configured, resource-capped set of alternative collections with explicit profile mappings.
- The query-time navigator may change only collection-compatible settings: prefetch limits, filters, fusion, thresholds, reranking, and final count.
- Every selection returns profile IDs, reason/confidence, fallback state, and provenance.

Full LLM, prompt, and generation evaluation remains outside this epic. TurboQuant remains exploratory until compatibility is proven.

## Epic 6 — Ollama Answer Generation With Citations

Tickets:

- `RAG-032`: Prompt assembly using navigator-selected retrieved chunks.
- `RAG-033`: Pinned Ollama-on-Colab runtime and generation client.
- `RAG-034`: Answer API with citations, retrieval profile, trace ID, and configuration provenance.
- `RAG-035`: Generation, insufficient-context, citation, navigator-integration, and mocked-boundary tests.

Finished state:

- Colab starts a pinned, self-managed Ollama runtime and calls it through an infrastructure adapter.
- Prompt assembly uses navigator-selected chunks and bounded context.
- Responses include answer text, citations, retrieval profile, trace ID, and configuration provenance.
- Insufficient context and runtime/model failures produce stable fallback behavior.

## Epic 7 — Local Gradio MVP

Tickets:

- `RAG-036`: Rehydrate and validate the Epic 5 selected configurations on the local Docker/Qdrant/Ollama runtime.
- `RAG-037`: Thin Gradio application skeleton.
- `RAG-038`: Document-upload flow.
- `RAG-039`: Question-and-answer flow.
- `RAG-040`: Citation, loading, empty, and error states.
- `RAG-041`: End-to-end local smoke tests and operating guide.

Finished state:

- Selected profiles rebuild and pass compatibility checks locally.
- Gradio calls FastAPI without duplicating backend business logic.
- The local workflow uploads, indexes, retrieves, reranks, generates, and displays cited answers.
- Operating guidance covers start, stop, rebuild, smoke testing, and troubleshooting.

The Phase 1 lean MVP is complete at the end of Epic 7.

## Phase 1 Acceptance Criteria

- Epics 2 through 6 are reproducible from a fresh free-tier Colab runtime and pinned project bootstrap.
- Supported documents produce stable dense/sparse Qdrant points with complete citation payloads.
- Qdrant hybrid retrieval and MiniLM reranking are tested before generation.
- Epic 5 produces reproducible evidence, validated profiles, a safe fallback, and the two-level navigator.
- Epic 6 generates cited answers with trace and configuration provenance.
- Epic 7 runs the same package logic and selected profiles locally through FastAPI, Qdrant, Ollama, and Gradio.
- No paid dependency, hosted vector database, committed secret, Drive-backed Qdrant storage, or notebook-only implementation is introduced.

## After Phase 1

Session memory is deferred to a future post-MVP plan without a Phase 1 epic number. The broader roadmap retains retrieval inspection and quality, documentation automation, the full evaluation engine, model routing and semantic cache, output arbitration, and the final React/Next.js interface.
