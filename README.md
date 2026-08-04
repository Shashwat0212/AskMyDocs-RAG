# AskMyDocs-RAG

AskMyDocs-RAG is a free and open-source RAGOps platform for document ingestion, Qdrant-native hybrid retrieval, reranking, cited answer generation, experiment-driven configuration, evaluation, semantic caching, model routing, arbitration, and documentation automation.

## Phase 1 Execution Model

- **Epic 1:** local FastAPI, Docker Qdrant, Ollama, and operations foundations.
- **Epics 2–6:** canonical development in free-tier Google Colab with pinned dependencies and ephemeral self-managed Qdrant/Ollama.
- **Epic 7:** return to local Docker/Qdrant/Ollama and deliver the Gradio MVP.

Git stores reviewed code, compact fixtures, selected profiles, manifests, and summaries. Configured shared Google Drive storage holds datasets and full experiment artifacts. Colab Qdrant data stays on the runtime filesystem and is rebuilt from source data and configuration.

## Project Constraints

- Use free and open-source components. Free Colab is the explicit hosted-compute exception.
- Do not depend on paid APIs, paid hosted inference, hosted vector databases, paid evaluation, paid observability, or paid experiment tracking.
- Keep notebooks thin and business logic portable between Colab and the local MVP runtime.
- Prefer configuration over hardcoded behavior and keep changes focused, tested, documented, and reviewable.

## Phase 1 Architecture

- Backend API: FastAPI
- MVP UI: Gradio; final UI: React / Next.js
- Retrieval: Qdrant named dense and sparse/BM25 vectors, native RRF/DBSF fusion, complete chunk/citation payloads
- Initial reranker: local `cross-encoder/ms-marco-MiniLM-L-6-v2`
- Model serving: Ollama, with Qwen3 4B as the initial generation baseline
- Dense embedding baseline: nomic-embed-text-v1.5, subject to Epic 5 evidence
- Local orchestration: Docker Compose for Epic 1 and Epic 7
- Evaluation: retrieval evidence in Epic 5; DeepEval and Ragas in the later full evaluation stage

SQLite is not part of the Phase 1 document retrieval path. Session memory is deferred until after the Phase 1 MVP.

## Read First

Before starting any task, read:

1. [starter.md](starter.md)
2. [AGENTS.md](AGENTS.md)

Then use the starter's task-routing table. The governing DOCX files under `docs/source_documents/` must be read before architecture, roadmap, stack, constraint, or stage-order changes.

## Current State

Day Zero is complete. Phase 1 Epic 1 is active. `RAG-001` is locally validated pending synchronization, and provisional `RAG-002` is in progress on Shashwat's feature branch. Future ticket references through `RAG-041` are planning identifiers until Jira confirms them. See `docs/PROJECT_STATUS.md` for the current snapshot.
