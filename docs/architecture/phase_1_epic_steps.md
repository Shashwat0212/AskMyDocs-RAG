# Phase 1 Epic Step Plan

## Purpose

This planning guide expands the seven-epic Phase 1 plan into delivery steps. The authoritative ticket list and acceptance criteria are in `phase_1_core_rag_mvp.md`. Ticket references not yet created in Jira are provisional.

## Runtime Sequence

```text
Epic 1: local foundations
  -> Epics 2-6: free-tier Colab, ephemeral Qdrant/Ollama
  -> Epic 7: local Docker/Qdrant/Ollama/Gradio MVP
```

Repository package code remains portable across both environments. Notebooks launch package entrypoints and capture diagnostics; they do not own business logic.

## Epic 1 — Local Backend Foundations (`RAG-001`–`RAG-004`)

1. Build and test the minimal FastAPI skeleton, health endpoint, typed settings, trace-aware logging, and backend sandbox.
2. Start pinned Qdrant through Docker Compose, verify readiness, collections, payloads, and vector-dimension constraints.
3. Verify the approved Ollama model and HTTP boundary locally.
4. Consolidate commands, checks, shutdown steps, and troubleshooting in operations guidance.

Document ingestion, backend indexing/retrieval, backend generation, and UI work remain out of scope until Epic 2.

## Epic 2 — Colab Environment and Document Ingestion (`RAG-005`–`RAG-010`)

1. Add one reproducible Colab bootstrap path that checks out the assigned branch, installs pinned dependencies, mounts the configured shared Drive location, and records runtime diagnostics.
2. Define `POST /api/v1/documents` and stable response/error contracts.
3. Validate PDF, TXT, and Markdown inputs and enforce the storage boundary: runtime filesystem for work, shared Drive for declared durable inputs/artifacts.
4. Extract text plus page or section metadata where available.
5. Route chunking through a configuration-selected strategy with explicit size, overlap, and metadata behavior.
6. Produce stable document/chunk IDs and focused validation, extraction, chunking, metadata, and bootstrap tests.

## Epic 3 — Qdrant Embedding and Indexing (`RAG-011`–`RAG-014`)

1. Define dense and sparse embedding interfaces that report model/version/dimension metadata.
2. Define named `dense` and `sparse` vectors and a complete retrievable payload containing chunk text, document/source IDs, order, and citation fields.
3. Create deterministic, collision-resistant collection names derived from corpus, ingestion/index profile, and version/run identity.
4. Index points through a Qdrant adapter and validate dimensions, distance, sparse compatibility, payload schema, and model/profile hashes.
5. Prove that an empty runtime can rebuild collections from source documents, manifests, and profiles.

There is no SQLite chunk store or SQLite lexical index in the Phase 1 document path.

## Epic 4 — Qdrant Hybrid Retrieval and Reranking (`RAG-015`–`RAG-021`)

1. Define the retrieval input/output contract, including filters, profile IDs, trace context, score components, payloads, and citations.
2. Embed the query and prefetch dense candidates from the named dense vector.
3. Produce Qdrant BM25/sparse query vectors and prefetch sparse candidates.
4. Fuse prefetches through the Qdrant Query API using RRF by default; retain DBSF as a configurable option.
5. Pass bounded Qdrant candidates to a configurable reranker interface.
6. Implement the initial local `cross-encoder/ms-marco-MiniLM-L-6-v2` adapter with timeout, disable, and fallback behavior.
7. Test dense, sparse, fusion, payload hydration, reranking, fallback, trace, and score-provenance paths before adding an LLM call.

## Epic 5 — Prototype Experimentation and Configuration Navigator (`RAG-022`–`RAG-031`)

1. Register each dataset with stable identity, checksum, query set, relevance judgments, license/source information, and Drive location.
2. Define ingestion/index profiles, query profiles, experiment search spaces, resource caps, and run manifests.
3. Start from the completed Epic 4 integration commit and record that SHA in every run. Expose plug-in boundaries without retaining a second permanent pipeline.
4. Build a manually launched Colab runner that expands configuration matrices, isolates failures, checkpoints to Drive, and resumes without silently duplicating runs.
5. Execute controlled multi-dataset experiments, changing parameters granularly enough to preserve causal interpretation.
6. Capture retrieval metrics, latency, indexing cost, memory, storage, errors, environment characteristics, and exact artifact locations.
7. Produce per-dataset/profile winners, Pareto trade-offs, validated profiles, and a conservative safe default.
8. Build the pre-ingestion scanner. It selects one index profile when confidence is adequate; otherwise it may create only a configured, resource-capped alternative set.
9. Build the query-time navigator for settings compatible with existing collections: candidate limits, filters, fusion, thresholds, reranking, and final count.
10. Merge validated plug-in interfaces, profiles, and navigator contracts into the product pipeline, then remove temporary duplicate prototype code.

Candidate experiment families include chunking, embedding models/supported dimensions, sparse models, distance, HNSW, optimizer settings, quantization, payload indexes, fusion, thresholds, candidate counts, filtering, and reranking. TurboQuant remains outside the approved candidates until compatibility is demonstrated.

## Epic 6 — Ollama Answer Generation With Citations (`RAG-032`–`RAG-035`)

1. Assemble bounded prompts from navigator-selected retrieved chunks and configuration-managed templates.
2. Start and diagnose a pinned self-managed Ollama runtime inside Colab.
3. Implement the generation adapter and answer API.
4. Return answer text, citations, retrieval/index profile IDs, trace ID, fallback state, and configuration provenance.
5. Test successful generation, insufficient context, citation mapping, navigator integration, timeouts, runtime failures, and mocked model boundaries.

## Epic 7 — Local Gradio MVP (`RAG-036`–`RAG-041`)

1. Rebuild selected collections locally using the versioned Epic 5 profiles and validate model, vector, payload, and Qdrant compatibility.
2. Add a thin Gradio shell that calls FastAPI.
3. Implement the upload flow and clear validation/progress states.
4. Implement the question-and-answer flow.
5. Display citations, retrieval/configuration provenance where appropriate, and loading, empty, insufficient-context, and error states.
6. Run the complete local upload → index → retrieve → rerank → generate → cite smoke test and publish operating guidance.

## Cross-Epic Delivery Rules

- Use the canonical runtime for the epic and record the versions actually tested.
- Qdrant data remains ephemeral in Colab and never points to mounted Drive.
- Checkpoint only declared manifests and artifacts to Drive; commit reviewed code, compact fixtures, selected profiles, and summary reports to Git.
- Keep every profile change versioned and benchmark-backed.
- Keep session memory outside Phase 1.
