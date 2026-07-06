# Decision Log

Record important architecture, tooling, model, workflow, and repository decisions here.

## Format

```text
Date: YYYY-MM-DD
Decision:
Rationale:
Consequences:
```

## Decisions

Date: 2026-07-02
Decision: Establish Day Zero foundation before feature development.
Rationale: The team will use multiple AI coding assistants and needs shared standards, status tracking, and repository structure before implementation begins.
Consequences: The repository starts with documentation, configuration examples, and placeholder folders only. Application features begin after a reviewed feature ticket.

Date: 2026-07-02
Decision: Use `AGENTS.md` as the canonical AI-agent instruction file.
Rationale: Codex, Claude, GitHub Copilot, and future tools need a shared source of project rules.
Consequences: Assistant-specific files should stay thin and point back to `AGENTS.md`.

Date: 2026-07-03
Decision: Scope Phase 1 to staged Core RAG MVP epics with lightweight hybrid retrieval.
Rationale: The project owner wants the MVP retrieval plan to include hybrid retrieval without pulling in Stage 2 reranking, inspection, or quality-mode complexity.
Consequences: Phase 1 will target dense vector retrieval plus a simple local lexical path with configurable fusion. Cross-encoder reranking, retrieval inspection UI, quality model mode, evaluation automation, caching, routing, arbitration, and the final React/Next.js interface remain outside Phase 1. The later 2026-07-05 decision merges the first two setup epics while preserving this scope boundary.

Date: 2026-07-03
Decision: Store the owner-provided Technical Design Document and Approach document in the repository under `docs/source_documents/`.
Rationale: The project rules treat these documents as the governing source of truth, so agents and contributors need stable repo-local paths.
Consequences: Future roadmap, architecture, workflow, and implementation changes must be checked against the DOCX source documents before proceeding.

Date: 2026-07-05
Decision: Establish `KNOWLEDGE.md` as the folder-level knowledge documentation convention.
Rationale: The project needs durable, local-first knowledge sharing so contributors and AI agents can understand what each folder currently contains and what related documentation must change with implementation work.
Consequences: Every project-owned folder should contain a `KNOWLEDGE.md` file. The repository root `KNOWLEDGE.md` maps child knowledge docs. Changes to code, configuration, scripts, documentation structure, or behavior must update affected folder-level knowledge docs in the same change, and folder structure changes must update the root map.

Date: 2026-07-05
Decision: Merge the Phase 1 backend foundation and local service infrastructure epics into a single Backend Foundations And Local Tooling Familiarization epic.
Rationale: The project owner wants the first Phase 1 work to combine developer familiarization, FastAPI backend setup, local Qdrant validation, local Ollama validation, and repeatable operations commands before product feature development begins.
Consequences: The first Phase 1 epic now covers tickets `RAG-001` through `RAG-006`. It remains setup-focused and documentation-driven where appropriate. Document upload, ingestion, embeddings, retrieval, answer generation, Gradio UI, deployment pipelines, and feature integrations remain outside this merged setup epic.
