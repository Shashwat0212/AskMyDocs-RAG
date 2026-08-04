# AI Agent Instructions

This file is the canonical entrypoint for every AI coding assistant working in this repository.

## Source Of Truth

The project is governed by the project-owner documents below:

1. `docs/source_documents/Technical Design Document_ Local-First RAGOps Platform.docx`
2. `docs/source_documents/Approach.docx`

The Technical Design filename is retained for stable links; its current title is **Technical Design Document: Colab-First Development and Local MVP Runtime**. Do not steer away from the governing documents. If a request conflicts with them, stop and identify the conflict before making changes.

## Start Every Run

Every agent must begin with:

1. `starter.md`
2. `AGENTS.md`

Use the task-routing table in `starter.md` to read the detailed documents relevant to the task. Read both governing DOCX files before changing architecture, roadmap direction, selected stack, project constraints, or stage ordering.

## Non-Negotiable Project Constraints

- Use free and open-source components.
- Phase 1 uses a runtime-specific execution model: Epic 1 is local, Epics 2 through 6 use free-tier Google Colab as the canonical development runtime, and Epic 7 returns to the local Docker/Qdrant/Ollama runtime for the Gradio MVP.
- Free-tier Colab is the explicit hosted-compute exception. Do not introduce paid LLM APIs, paid hosted inference, hosted vector databases, paid evaluation services, paid observability platforms, or paid experiment tracking.
- Run Qdrant and Ollama as self-managed processes. During Epics 2 through 6 their Colab instances are ephemeral and pinned by the project bootstrap.
- Store Colab Qdrant data only on the runtime filesystem, never directly on mounted Google Drive. Rebuild collections from source datasets, manifests, and configuration.
- Keep reviewed code, compact fixtures, selected profiles, manifests, and summary reports in Git. Keep datasets and full experiment artifacts in the configured shared Drive location.
- Keep notebooks thin: business logic belongs in importable packages and must also run in the local Epic 7 runtime.
- Prefer configuration over hardcoded behavior and keep business logic separated from Colab, Drive, Docker, Qdrant, Ollama, API, and UI adapters.
- Keep changes focused to the assigned ticket. Update tests, documentation, and affected folder-level `KNOWLEDGE.md` files in the same change.
- Do not add feature code during repository-foundation or governance tasks.

## Target Architecture Direction

- Backend API: FastAPI
- MVP interface: Gradio on the local Epic 7 runtime
- Final interface: React / Next.js
- Model serving: Ollama; llama.cpp may be evaluated later where needed
- Document retrieval: self-managed Qdrant with named dense and sparse/BM25 vectors, native Query API fusion, complete retrievable chunk payloads, filters, and citation metadata
- Initial fusion: RRF; DBSF remains configurable
- Initial reranker: local `cross-encoder/ms-marco-MiniLM-L-6-v2`, integrated in Epic 4
- Experimentation and configuration navigator: Epic 5, before generation
- Evaluation: retrieval metrics in Epic 5; DeepEval and Ragas in the later Evaluation Engine stage
- Local orchestration: Docker Compose for Epic 1 and Epic 7
- Static reporting: GitHub Pages at the approved later stage
- CI: GitHub Actions at the approved later stage

SQLite is not a Phase 1 document-retrieval engine or canonical chunk store. Session memory is outside Phase 1 and may later use a separately approved local persistence design.

## Required Agent Workflow

1. Read `starter.md`, this file, and the task-specific sources routed from the starter.
2. Use synchronized `project-governance` for planning work, create approved epic integration branches from `main`, and create ticket branches from the latest active epic branch.
3. Inspect the current implementation and preserve unrelated user changes.
4. Confirm the ticket's canonical runtime and artifact boundary.
5. Identify impacted modules, configuration, tests, and documentation.
6. Keep the change small and reviewable, using existing structure and conventions.
7. Run relevant tests in the canonical runtime for the epic; document free-tier or environmental limitations.
8. Update affected folder-level `KNOWLEDGE.md` files and the root map when folder structure changes.
9. Update `starter.md`, `docs/PROJECT_STATUS.md`, `docs/FUTURE_PROSPECTS.md`, and `docs/DECISIONS.md` when their summaries or decisions change.
10. Summarize changes, tests, runtime, and artifact updates.

## Prohibited Without Explicit Approval

- Replacing the selected stack or the approved Phase 1 runtime sequence.
- Adding paid or hosted model, vector, evaluation, observability, or experiment-tracking dependencies.
- Persisting Qdrant directly on mounted Drive.
- Implementing unrelated features or notebook-only business logic.
- Committing secrets, large run artifacts, or datasets that belong in shared Drive.
- Adding undocumented temporary workarounds or retaining the Epic 5 copied prototype as a permanent second implementation.
- Creating deployment pipelines before the approved deployment stage.
