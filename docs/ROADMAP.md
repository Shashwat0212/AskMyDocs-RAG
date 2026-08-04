# Roadmap

The roadmap follows the governing Technical Design Document and Approach document.

## Stage 0 — Day Zero Foundation

Prepare repository structure, engineering workflow, documentation standards, AI-agent synchronization, and environment guidance. Completed.

## Stage 1 — Core RAG MVP (Phase 1)

Phase 1 follows a deliberate runtime transition:

1. **Epic 1 — Local Backend Foundations (`RAG-001`–`RAG-004`)**: FastAPI sandbox, local Docker Qdrant, local Ollama, and repeatable operations.
2. **Epic 2 — Colab Environment and Document Ingestion (`RAG-005`–`RAG-010`)**: pinned Colab bootstrap, Drive boundary, upload, extraction, configurable chunking, and stable metadata.
3. **Epic 3 — Qdrant Embedding and Indexing (`RAG-011`–`RAG-014`)**: dense/sparse interfaces, named vectors, complete chunk/citation payloads, deterministic collections, and rebuild tests.
4. **Epic 4 — Qdrant Hybrid Retrieval and Reranking (`RAG-015`–`RAG-021`)**: Qdrant dense and BM25/sparse retrieval, native Query API fusion, configurable MiniLM reranking, fallbacks, and traces.
5. **Epic 5 — Prototype Experimentation and Configuration Navigator (`RAG-022`–`RAG-031`)**: multi-dataset experiments, reproducible manifests, validated profiles, pre-ingestion scanner, query-time navigator, and merge-back of proven plug-in architecture.
6. **Epic 6 — Ollama Answer Generation With Citations (`RAG-032`–`RAG-035`)**: pinned Ollama in Colab, prompt assembly, cited answer API, profile/trace provenance, and failure tests.
7. **Epic 7 — Local Gradio MVP (`RAG-036`–`RAG-041`)**: rehydrate selected profiles locally, implement thin upload/QA flows, display citations and states, and complete the local end-to-end smoke test.

Epic 1 runs locally. Epics 2 through 6 run canonically on free-tier Colab with self-managed ephemeral Qdrant and, in Epic 6, Ollama. Epic 7 returns to local Docker/Qdrant/Ollama. The Phase 1 MVP is complete after Epic 7.

Qdrant is the only Phase 1 document retrieval engine. It owns named dense/sparse vectors, BM25/sparse retrieval, fusion, full retrievable chunk payloads, filters, and citation metadata. SQLite is not part of the Phase 1 document path.

Colab collections are disposable. Git stores reviewed code, compact fixtures, profiles, manifests, and summary reports; configured shared Drive storage holds datasets and full experiment artifacts. Qdrant storage never points directly at mounted Drive.

The detailed plan is in `docs/architecture/phase_1_core_rag_mvp.md` and `docs/architecture/phase_1_epic_steps.md`. Ticket references not yet created in Jira are provisional.

Session memory is a future post-MVP item without a Phase 1 epic number.

## Stage 2 — Retrieval Inspection And Quality Layer

- Retrieved chunk and score viewer
- Citation inspection panel
- Prompt/context preview
- Retrieval and configuration trace inspection
- Higher-quality generation mode

Core reranking is already delivered in Phase 1 Epic 4; this stage focuses on inspection, debugging, and broader quality experience.

## Stage 3 — Documentation Automation

- Changed-file and contract detector
- FastAPI route, configuration, and schema change detection
- Documentation impact mapper
- Markdown patch or review-artifact generation

## Stage 4 — Evaluation Engine

- End-to-end RAG evaluation dataset format
- Local judge integration
- Ragas metric pipeline
- DeepEval regression tests
- Generation/prompt comparison inputs and outputs
- JSON plus static HTML/Markdown reports
- GitHub Pages publishing at the approved deployment stage

Epic 5 provides retrieval-only experimental evidence; this stage adds full answer-quality and generation evaluation.

## Stage 5 — Multi-Model Routing And Semantic Cache

- Configuration-aware model routing
- Qdrant semantic cache collection
- Cache lookup, invalidation, and trace logging
- Cache inspection view

## Stage 6 — Output Arbitration

- Arbitration router
- Critic and judge prompts
- Structured arbitration output
- Retry/rewrite workflow
- Trace logging and UI visibility
