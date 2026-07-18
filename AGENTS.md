# AI Agent Instructions

This file is the canonical entrypoint for all AI coding assistants working in this repository, including Codex, Claude, GitHub Copilot, and future tools.

## Source Of Truth

The project is governed by the Technical Design Document and Approach document provided by the project owner:

1. `docs/source_documents/Technical Design Document_ Local-First RAGOps Platform.docx`
2. `docs/source_documents/Approach.docx`

Do not steer away from those documents. If a request conflicts with them, stop and call out the conflict before making changes.

## Start Every Run

Every agent must begin with:

1. `starter.md`
2. `AGENTS.md`

Use the task-routing table in `starter.md` to read the detailed documents relevant to the current task before modifying code or docs. Read both governing DOCX files before changing architecture, roadmap direction, selected stack, project constraints, or stage ordering.

## Non-Negotiable Project Constraints

- Local-first only.
- Use free and open-source components.
- Do not introduce paid LLM APIs, paid hosted inference, paid vector databases, paid evaluation services, or paid observability platforms.
- Prefer configuration over hardcoded behavior.
- Keep business logic separated from infrastructure concerns.
- Keep changes focused to the assigned ticket.
- Update documentation in the same change as implementation.
- Update affected folder-level `KNOWLEDGE.md` files in the same change as code, configuration, scripts, documentation structure, or behavior changes.
- Do not add feature code during repository-foundation tasks.

## Target Architecture Direction

- Backend API: FastAPI
- MVP interface: Gradio
- Final interface: React / Next.js
- Model serving: Ollama, then llama.cpp where needed
- Vector store: Qdrant
- Evaluation: DeepEval and Ragas
- Local deployment: Docker Compose
- Static reporting: GitHub Pages
- CI: GitHub Actions

## Required Agent Workflow

1. Read `starter.md`, this file, and the task-specific sources routed from the starter.
2. Use the synchronized `project-governance` branch for planning work, create approved epic integration branches from `main`, and create ticket implementation branches from the latest active epic branch.
3. Inspect existing implementation before proposing changes.
4. Identify impacted modules and documentation.
5. Keep the change small and reviewable.
6. Prefer existing structure and conventions.
7. Add or update tests when implementation exists.
8. Update affected folder-level `KNOWLEDGE.md` files and the root `KNOWLEDGE.md` map when folder structure changes.
9. Update `starter.md` when its current-state summary changes.
10. Update relevant docs, especially `docs/PROJECT_STATUS.md`, `docs/FUTURE_PROSPECTS.md`, and `docs/DECISIONS.md` when applicable.
11. Summarize changes, tests, and documentation updates.

## Prohibited Without Explicit Approval

- Replacing the selected stack.
- Adding hosted paid dependencies.
- Implementing unrelated features.
- Committing secrets.
- Adding temporary workarounds without documenting the reason.
- Creating deployment pipelines before the approved deployment stage.
