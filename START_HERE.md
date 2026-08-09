# AskMyDocs-RAG Governance Briefing

Last reviewed: 2026-08-09

Read this file first whenever working on `project-governance`, followed by
[AGENTS.md](AGENTS.md).

## Current State

- Day Zero foundation is complete.
- Phase 1 Epic 1 is active.
- `RAG-001` implementation and local validation are complete, with project
  tracking synchronization still pending.
- Provisional `RAG-002` is in progress on
  `feature/shashwat/RAG-002-qdrant-sandbox`.
- `RAG-003` and `RAG-004` remain planned and provisional until Jira confirms
  their keys.
- No project blocker is recorded.

## Approved Phase 1 Sequence

| Epic | Tickets | Runtime | Outcome |
|---|---|---|---|
| 1 — Local Foundations | `RAG-001`–`RAG-004` | Local | FastAPI, Qdrant, Ollama, and operations foundations |
| 2 — Document Ingestion | `RAG-005`–`RAG-010` | Colab | Stable extraction, chunking, and metadata |
| 3 — Indexing and Retrieval | `RAG-011`–`RAG-021` | Colab | Dense/sparse indexing, fusion, reranking, and traces |
| 4 — Retrieval Evaluation | `RAG-022`–`RAG-028` | Colab | Golden benchmark and retrieval baselines |
| 5 — Profiles and Navigator | `RAG-029`–`RAG-037` | Colab | Validated profiles and profile selectors |
| 6 — Answer Generation | `RAG-038`–`RAG-041` | Colab | Ollama answers with citations and provenance |
| 7 — Local Gradio MVP | `RAG-042`–`RAG-047` | Local | Complete local upload-to-answer workflow |

Ticket references after the confirmed Jira work are planning identifiers until
Jira creates them.

## Evaluation Direction

Phase 1 makes benchmark-backed claims about retrieval, not broad claims about
LLM answer quality. Epic 4 creates 300 human-approved questions across three
document families and three corpus sizes. Epic 5 compares configurations and
trains two small decision trees:

- A corpus navigator chooses an ingestion/index profile before indexing.
- A query navigator chooses a compatible retrieval profile for each question.

Low-confidence or incompatible selections use a versioned `safe-default`
profile and record the reason.

## Project Constraints

- Local-first and free/open-source only.
- Free-tier Colab is the approved shared runtime for Epics 2–6.
- Qdrant and Ollama remain self-managed.
- No paid APIs, hosted vector databases, paid evaluation, or paid observability.
- Notebooks are thin launchers over importable package code.
- Configuration is preferred over hardcoded behavior.
- No application code is implemented on this branch.

## Where To Read Next

| Need | Read |
|---|---|
| Current work and blockers | [Status](governance/current/STATUS.md) |
| Tracking and promotion workflow | [Tracking](governance/current/TRACKING.md) |
| Complete stage sequence | [Roadmap](governance/roadmap/ROADMAP.md) |
| Phase 1 details | [Phase 1 index](governance/phase-1/README.md) |
| Retrieval benchmark | [Epic 4](governance/phase-1/EPIC-04-RETRIEVAL-EVALUATION.md) |
| Profiles and navigators | [Epic 5](governance/phase-1/EPIC-05-PROFILES-AND-NAVIGATOR.md) |
| Accepted and superseded choices | [Decision log](governance/decisions/DECISIONS.md) |
| Engineering rules | [Standards](governance/standards/ENGINEERING-WORKFLOW.md) |
| Governing owner documents | [Sources](governance/sources/README.md) |

## Branch Workflow

`project-governance` is a standalone planning branch. It is not merged into
`main`. Approved plans are selectively promoted through
[handoffs](governance/handoffs/README.md). Application branches continue to
follow the epic and ticket workflow defined by the implementation repository.
