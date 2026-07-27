# AskMyDocs-RAG Starter Briefing

Last reviewed: 2026-07-27
Maintained through: `project-governance`

Read this file first at the start of every human or AI work session. Then read `AGENTS.md` and use the task-routing table below to load the detailed sources needed for the current task.

This file is a maintained orientation snapshot. It does not replace the governing source documents, project status, roadmap, architecture plans, or decision log.

## Project Purpose

AskMyDocs-RAG is a local-first RAGOps platform for document ingestion, retrieval, cited answer generation, evaluation, semantic caching, model routing, arbitration, and automated documentation updates.

Non-negotiable constraints:

- Use free and open-source, local-first components.
- Do not introduce paid LLM APIs, hosted inference, hosted vector databases, paid evaluation services, or paid observability platforms.
- Prefer configuration over hardcoded behavior.
- Keep business logic separate from infrastructure concerns.
- Keep implementation work inside an approved ticket and update tests, documentation, and affected `KNOWLEDGE.md` files together.
- Governance-only updates do not require a placeholder Jira ticket; reference a ticket when the update relates to one.

## Current State

- Day Zero foundation is complete and merged.
- The repository contains standards, plans, placeholders, example configuration, and setup guidance.
- The approved baseline contains no FastAPI product application, frontend application, retrieval pipeline, model integration, evaluation engine, or Docker Compose service definition.
- Phase 1 execution is starting with Epic 1: Backend Foundations And Local Tooling Familiarization.
- The Epic 1 integration branch is `epic/epic-1-backend-foundations`.
- `RAG-001`, the combined FastAPI tutorial and backend sandbox, is assigned to Shashwat; implementation and local validation are complete on its feature branch, while Jira synchronization remains pending.
- Provisional `RAG-002`, the Docker Compose and Qdrant local sandbox, is assigned to Shashwat and ready on `feature/shashwat/RAG-002-qdrant-sandbox`; confirm the key in Jira before implementation.
- The remaining Ollama and operations tickets are approved templates awaiting Jira keys and assignment.
- No project blocker is currently recorded.

## Active Ticket: RAG-002

Title: Docker Compose And Qdrant Local Sandbox

Branch: `feature/shashwat/RAG-002-qdrant-sandbox`

Objective: Confirm developers can independently start, inspect, use, stop, and troubleshoot local Qdrant.

Task:

- Add a minimal Docker Compose service using a pinned Qdrant image.
- Configure local persistence and readiness checking.
- Practice collection creation, vector upsert, similarity search, and deletion.
- Verify that normal shutdown preserves stored data.
- Document start, stop, logs, health, persistence, and destructive reset commands.
- Keep backend Qdrant integration, embeddings, ingestion, retrieval, and production deployment out of scope.

Acceptance criteria:

- Docker Compose configuration is valid.
- Qdrant starts and becomes ready.
- Collection creation, upsert, search, and deletion succeed.
- Normal shutdown preserves stored data.
- Destructive reset is clearly identified.
- No backend Qdrant integration is added.

Learning references:

- [Qdrant 101: Getting Started](https://youtu.be/LRcZ9pbGnno)
- [Qdrant local quickstart](https://qdrant.tech/documentation/quick-start/)
- [Docker Compose documentation](https://docs.docker.com/compose/)

## Next Work

1. Create or link the Jira work item and confirm the provisional `RAG-002` key.
2. Verify Docker and Docker Compose prerequisites.
3. Select and pin a Qdrant image version.
4. Add the isolated Compose service, persistence volume, and readiness check.
5. Run and record the collection, upsert, search, deletion, restart, and reset exercises.
6. Add operating instructions and validate the acceptance criteria without backend integration.

## Branch Model

- `project-governance` is the permanent working branch for current status, Jira summaries, future prospects, plans, and proposed decisions.
- `main` contains approved governance checkpoints and is the base for epic integration branches.
- Epic branches use `epic/<epic-id>-short-description`, integrate the epic's ticket work, and merge into `main`.
- Ticket branches start from the latest epic branch, use `feature/<developer>/<ticket-id>-short-description`, and merge back into that epic branch.
- The active Epic 1 branch is `epic/epic-1-backend-foundations`; the current ticket branch is `feature/shashwat/RAG-002-qdrant-sandbox`.
- Application code must not be implemented on `project-governance`.
- Governance pull requests into `main` use merge commits so the permanent branch retains shared ancestry.

## Phase 1 Epic Map

| Epic | Name | Delivery point |
|---|---|---|
| 1 | Backend Foundations And Local Tooling Familiarization | Setup and learning |
| 2 | Document Ingestion Pipeline | Lean MVP |
| 3 | Embedding And Vector Indexing | Lean MVP |
| 4 | Hybrid Retrieval Pipeline | Lean MVP |
| 5 | Answer Generation With Citations | Lean MVP |
| 6 | MVP Gradio Interface | Lean MVP complete |
| 7 | Reranking And Retrieval Quality | Post-MVP Phase 1 enhancement |
| 8 | Session Memory And Conversation Retrieval | Post-MVP Phase 1 enhancement |
| 9 | Hyperparameter Experimentation And Blueprinting | Post-MVP Phase 1 enhancement |

Epics 1 through 6 deliver the first lean MVP. Epics 7 through 9 are approved Phase 1 enhancements that begin only after the Gradio MVP is working.

Broader Stages 2 through 6 remain retrieval inspection and quality, documentation automation, evaluation, model routing and semantic cache, and output arbitration. They are outside the current Phase 1 implementation scope.

## Approved Stack

- Backend API: FastAPI
- MVP interface: Gradio
- Final interface: React / Next.js
- Model serving: Ollama first, llama.cpp where needed
- Vector store: Qdrant
- Canonical local records and lexical search: SQLite and SQLite FTS5/BM25
- Main generation model: Qwen3 4B
- Main embedding model: nomic-embed-text-v1.5
- Evaluation: DeepEval and Ragas
- Local orchestration: Docker Compose
- Observability direction: OpenTelemetry, Prometheus, and Grafana OSS
- CI and static publishing: GitHub Actions and GitHub Pages at their approved roadmap stages

## Active Decisions To Preserve

- One user workflow carries one `trace_id` through its complete backend flow.
- Logs and spans are trace-aware; VizTracer is optional local profiling, not always-on tracing.
- Chunking and retrieval behavior are configurable strategies and tunable hyperparameters.
- SQLite is the expected canonical chunk store.
- Qdrant is the dense vector index with lightweight payloads, not the canonical full-text store.
- SQLite FTS5/BM25 is the local lexical index over the same stable chunk IDs.
- `project-governance` and `main` use the documented two-way synchronization workflow.
- Approved implementation work uses short-lived epic integration branches with developer-namespaced ticket branches.
- Future ideas belong in `docs/FUTURE_PROSPECTS.md`; only approved choices belong in the roadmap, architecture plans, and decision log.

## Source Hierarchy

1. Project-owner source documents under `docs/source_documents/` govern project intent.
2. `AGENTS.md` governs repository-wide agent behavior.
3. `docs/DECISIONS.md` records accepted and superseded decisions.
4. `docs/ROADMAP.md` and `docs/architecture/` define approved sequencing and scope.
5. `docs/PROJECT_STATUS.md` records the current project snapshot.
6. This starter summarizes those sources for orientation and must be corrected when it drifts.

Read both governing DOCX files before changing architecture, roadmap direction, selected stack, project constraints, or stage ordering:

- `docs/source_documents/Technical Design Document_ Local-First RAGOps Platform.docx`
- `docs/source_documents/Approach.docx`

## Task Routing

| Task | Read after this file and `AGENTS.md` |
|---|---|
| Current status or next work | `docs/PROJECT_STATUS.md`, `docs/PROJECT_TRACKING.md` |
| Epic, sprint, Jira, or future planning | `docs/PROJECT_STATUS.md`, `docs/PROJECT_TRACKING.md`, `docs/FUTURE_PROSPECTS.md`, `docs/ROADMAP.md`, relevant `docs/architecture/` plans |
| Architecture, stack, constraints, or stage changes | Both governing DOCX files, `docs/ROADMAP.md`, `docs/DECISIONS.md`, relevant architecture plans |
| Implementation | Active Jira ticket, `docs/ENGINEERING_WORKFLOW.md`, `docs/CODING_STANDARDS.md`, relevant folder `KNOWLEDGE.md`, relevant API/architecture/operations docs |
| Local environment or setup | `docs/DEVELOPMENT_ENVIRONMENT.md`, `docs/operations/day_zero_setup.md` |
| Branches, pull requests, or completion | `docs/ENGINEERING_WORKFLOW.md`, `docs/PROJECT_TRACKING.md`, `.github/pull_request_template.md` |
| Configuration | `.env.example`, `configs/README.md`, `configs/KNOWLEDGE.md`, relevant example YAML files |
| AI-agent workflow | `docs/AI_AGENT_WORKFLOW.md`, relevant assistant adapter |

## Start-Of-Run Checklist

1. Read this file and `AGENTS.md`.
2. Run `git status --short --branch` and preserve unrelated user changes.
3. Confirm the active branch matches the task: planning on synchronized `project-governance`, epic integration from `main`, and ticket implementation from the latest active epic branch.
4. Read the task-specific sources from the routing table.
5. Inspect existing files before proposing or editing.
6. Confirm the ticket, scope, acceptance criteria, tests, and documentation impact.
7. Do not add feature code while performing planning or repository-foundation work.

## Maintenance Contract

Update this file in the same governance change when any of these changes:

- current phase or active epic
- next ticket or sprint sequence
- Jira work-item status at the project-summary level
- branch or project-tracking policy
- approved stack or local-first constraints
- implemented repository shape or available runtime entrypoints
- major active decision summarized here
- epic count, names, ordering, or MVP boundary

Keep detailed reasoning in the source documents and decision log. Keep this file concise enough to read at the beginning of every run.
