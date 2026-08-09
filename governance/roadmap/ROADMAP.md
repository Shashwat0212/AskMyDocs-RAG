# Roadmap

Last reviewed: 2026-08-09

## Stage 0 — Foundation

Repository setup, working agreements, initial documentation, and local environment guidance. Complete.

## Phase 1 — Core RAG MVP

1. **Epic 1 — Local Foundations (`RAG-001`–`RAG-004`)**: learn and validate FastAPI, Docker Qdrant, Ollama, and repeatable local operations.
2. **Epic 2 — Document Ingestion (`RAG-005`–`RAG-010`)**: create the Colab bootstrap, upload contract, validation, extraction, chunking, metadata, and tests.
3. **Epic 3 — Indexing and Retrieval (`RAG-011`–`RAG-021`)**: build dense and sparse Qdrant indexes, hybrid fusion, MiniLM reranking, and retrieval traces.
4. **Epic 4 — Retrieval Evaluation (`RAG-022`–`RAG-028`)**: build the scale-aware golden benchmark and establish retrieval baselines.
5. **Epic 5 — Profiles and Navigator (`RAG-029`–`RAG-037`)**: compare bounded configuration sets, promote versioned profiles, and train the ingestion and query decision trees.
6. **Epic 6 — Answer Generation (`RAG-038`–`RAG-041`)**: assemble context, call Ollama, return cited answers, and test model-boundary failures.
7. **Epic 7 — Local Gradio MVP (`RAG-042`–`RAG-047`)**: rehydrate selected profiles locally and deliver the upload-to-cited-answer interface.

Epic 1 runs locally. Epics 2–6 run canonically in free-tier Colab with self-managed ephemeral Qdrant and, in Epic 6, Ollama. Epic 7 returns to local Docker/Qdrant/Ollama.

Qdrant is the only Phase 1 document retrieval engine. SQLite is not used in the Phase 1 document path. Full answer-quality model comparison is not part of Phase 1; retrieval is the primary benchmarked engineering output.

## Stage 2 — Retrieval Inspection And Quality Experience

- Retrieved chunk and score viewer.
- Citation inspection.
- Prompt and context preview.
- Retrieval/configuration trace inspection.
- Higher-quality generation mode where hardware allows.

## Stage 3 — Documentation Automation

- Changed-file and contract detection.
- Route, configuration, and schema impact mapping.
- Markdown patch or review-artifact generation.

## Stage 4 — Generation And System Evaluation

- Local judge integration.
- Ragas and DeepEval pipelines where appropriate.
- Prompt and model comparison.
- Answer faithfulness, completeness, relevance, and citation evaluation.
- Static reports and regression publication.

Epic 4 provides deterministic retrieval evaluation. This later stage evaluates model-dependent generated answers and the complete system.

## Stage 5 — Model Routing And Semantic Cache

- Configuration-aware model routing.
- Qdrant semantic cache.
- Cache invalidation, traces, and inspection.

## Stage 6 — Output Arbitration

- Critic and judge workflows.
- Retry or rewrite behavior.
- Arbitration traces and UI visibility.

Session memory, the final React/Next.js interface, and additional research ideas remain post-MVP work unless separately approved.
