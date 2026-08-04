# AskMyDocs-RAG Starter Briefing

Last reviewed: 2026-08-04
Maintained through: `project-governance`

Read this file first at the start of every human or AI work session. Then read `AGENTS.md` and use the task-routing table below. This is an orientation snapshot, not a replacement for the governing source documents, project status, roadmap, architecture plans, or decision log.

## Project Purpose

AskMyDocs-RAG is a free and open-source RAGOps platform. Phase 1 uses local tooling for Epic 1, free-tier Google Colab as the canonical shared development environment for Epics 2 through 6, and a local Docker/Qdrant/Ollama runtime for the final Gradio MVP in Epic 7.

Non-negotiable constraints:

- Use only free and open-source components; free-tier Colab is the explicit hosted-compute exception.
- Do not introduce paid APIs, paid hosted inference, hosted vector databases, paid evaluation, paid observability, or paid experiment tracking.
- Qdrant and Ollama remain self-managed. Colab instances are ephemeral and reproducible.
- Store code/configuration/summaries in Git, datasets and full experiment artifacts in shared Drive, and Colab Qdrant storage only on the runtime filesystem.
- Keep notebooks thin, behavior configurable, business logic infrastructure-independent, and changes scoped to an approved ticket.

## Current State

- Day Zero foundation is complete and merged.
- Phase 1 is executing Epic 1, **Local Backend Foundations**, unchanged under its local scope.
- `RAG-001` implementation and local validation are complete; Jira and repository disposition remain to be synchronized.
- Provisional `RAG-002`, the Docker Compose and Qdrant local sandbox, is assigned to Shashwat and is actively being developed on `feature/shashwat/RAG-002-qdrant-sandbox` with uncommitted work that must be preserved.
- `RAG-003` and `RAG-004` are planned Epic 1 tickets awaiting Jira confirmation.
- The approved Phase 1 plan now contains seven epics and 41 sequential references. References not yet created in Jira are provisional.
- No project blocker is recorded.

## Next Work

1. Preserve and finish the active `RAG-002` local Qdrant sandbox.
2. Synchronize `RAG-001` and provisional `RAG-002` with Jira.
3. Create and assign provisional `RAG-003` and `RAG-004`.
4. Complete and validate Epic 1 locally.
5. Begin `RAG-005`, the reproducible Colab bootstrap, only after Epic 1 closes.

## Branch Model

- `project-governance` is the permanent branch for project state, planning, prospects, and decisions; application code is not implemented there.
- `main` contains approved governance checkpoints and is the base for epic integration branches.
- Epic branches use `epic/<epic-id>-short-description`; ticket branches start from the latest epic branch and use `feature/<developer>/<ticket-id>-short-description`.
- The active Epic 1 branch is `epic/epic-1-backend-foundations`.
- Epic 5 uses its integration branch as the isolated experiment snapshot; every run manifest records the exact source commit. Validated interfaces and profiles merge back, and temporary duplicate prototype code is removed.

## Phase 1 Epic Map

| Epic | Name | Tickets | Canonical runtime | Delivery point |
|---|---|---|---|---|
| 1 | Local Backend Foundations | `RAG-001`–`RAG-004` | Local | Local foundations complete |
| 2 | Colab Environment and Document Ingestion | `RAG-005`–`RAG-010` | Free-tier Colab | Reproducible ingestion |
| 3 | Qdrant Embedding and Indexing | `RAG-011`–`RAG-014` | Free-tier Colab | Rebuildable dense/sparse indexes |
| 4 | Qdrant Hybrid Retrieval and Reranking | `RAG-015`–`RAG-021` | Free-tier Colab | Retrieval before LLM integration |
| 5 | Prototype Experimentation and Configuration Navigator | `RAG-022`–`RAG-031` | Free-tier Colab | Evidence-backed profiles and navigator |
| 6 | Ollama Answer Generation With Citations | `RAG-032`–`RAG-035` | Free-tier Colab | Cited generation with provenance |
| 7 | Local Gradio MVP | `RAG-036`–`RAG-041` | Local | Phase 1 MVP complete |

Session memory is a future post-MVP item without a Phase 1 epic number. Broader Stages 2 through 6 remain retrieval inspection and quality, documentation automation, evaluation, model routing and semantic cache, and output arbitration.

## Approved Stack And Boundaries

- Backend API: FastAPI
- MVP interface: Gradio; final interface: React / Next.js
- Model serving: Ollama first; llama.cpp may be evaluated later
- Retrieval: Qdrant named dense and sparse/BM25 vectors, full chunk/citation payloads, Query API fusion with RRF initially and DBSF configurable
- Reranking: configurable local MiniLM cross-encoder in Epic 4
- Main generation model: Qwen3 4B
- Initial dense embedding model: nomic-embed-text-v1.5, subject to Epic 5 evidence
- Evaluation: retrieval metrics in Epic 5; DeepEval and Ragas later
- Local orchestration: Docker Compose for Epic 1 and Epic 7

SQLite is not part of Phase 1 document retrieval. Ephemeral Qdrant collections are rebuilt from source documents, dataset manifests, and versioned profiles.

## Active Decisions To Preserve

- One user workflow carries one `trace_id` through its backend flow.
- Chunking, indexing, retrieval, fusion, filtering, and reranking use configurable strategy boundaries.
- Three configuration contracts govern the pipeline: ingestion/index profile, query profile, and run manifest.
- The pre-ingestion scanner may select one index profile or a resource-capped alternative set when uncertain. The query-time navigator may change only settings compatible with existing collections.
- Colab experiment workflows are manually launched, automated end to end, checkpointed, resumable, and failure-isolated; they are not unattended schedules.
- Future ideas stay in `docs/FUTURE_PROSPECTS.md` until approved and promoted.

## Source Hierarchy

1. Governing project-owner DOCX files under `docs/source_documents/`.
2. `AGENTS.md` for repository-wide agent behavior.
3. `docs/DECISIONS.md` for accepted and superseded decisions.
4. `docs/ROADMAP.md` and `docs/architecture/` for approved sequencing and scope.
5. `docs/PROJECT_STATUS.md` for the current project snapshot.
6. This starter for orientation.

Read both governing DOCX files before changing architecture, roadmap direction, selected stack, project constraints, or stage ordering:

- `docs/source_documents/Technical Design Document_ Local-First RAGOps Platform.docx`
- `docs/source_documents/Approach.docx`

## Task Routing

| Task | Read after this file and `AGENTS.md` |
|---|---|
| Current status or next work | `docs/PROJECT_STATUS.md`, `docs/PROJECT_TRACKING.md` |
| Epic, sprint, Jira, or future planning | Project status/tracking, `docs/FUTURE_PROSPECTS.md`, `docs/ROADMAP.md`, relevant architecture plan |
| Architecture, stack, constraints, or stage changes | Both governing DOCX files, roadmap, decisions, relevant architecture plans |
| Implementation | Active Jira ticket, engineering workflow, coding standards, relevant knowledge/API/architecture/operations docs |
| Local or Colab environment/setup | `docs/DEVELOPMENT_ENVIRONMENT.md`, `docs/operations/day_zero_setup.md` |
| Branches, pull requests, or completion | `docs/ENGINEERING_WORKFLOW.md`, `docs/PROJECT_TRACKING.md`, pull-request template |
| Configuration or experiment profiles | `.env.example`, `configs/README.md`, `configs/KNOWLEDGE.md`, relevant YAML, Epic 5 architecture |
| AI-agent workflow | `docs/AI_AGENT_WORKFLOW.md`, relevant assistant adapter |

## Start-Of-Run Checklist

1. Read this file and `AGENTS.md`.
2. Run `git status --short --branch` and preserve unrelated user changes.
3. Confirm the branch, ticket, canonical runtime, and artifact boundary.
4. Load task-specific sources from the routing table and inspect existing implementation.
5. Confirm acceptance criteria, tests, documentation, and knowledge impact.
6. Do not add feature code during governance or repository-foundation work.

## Maintenance Contract

Update this file whenever the current phase, next work, Jira summary, branch policy, stack, runtime boundary, repository shape, major decision, epic sequence, or MVP boundary changes. Keep detailed reasoning in the governing sources and decision log.
