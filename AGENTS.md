# AI Agent Instructions

This file is the canonical entrypoint for all AI coding assistants working in this repository, including Codex, Claude, GitHub Copilot, and future tools.

## Source Of Truth

The project is governed by the Technical Design Document and Approach document provided by the project owner:

1. `docs/source_documents/Technical Design Document_ Local-First RAGOps Platform.docx`
2. `docs/source_documents/Approach.docx`

Do not steer away from those documents. If a request conflicts with them, stop and call out the conflict before making changes.

## Read Before Coding

Every agent must read these files before modifying code or docs:

1. `README.md`
2. `KNOWLEDGE.md`
3. `docs/PROJECT_STATUS.md`
4. `docs/PROJECT_TRACKING.md`
5. `docs/FUTURE_PROSPECTS.md` for planning and future-epic tasks
6. `docs/ROADMAP.md`
7. `docs/ENGINEERING_WORKFLOW.md`
8. `docs/DEVELOPMENT_ENVIRONMENT.md`
9. `docs/CODING_STANDARDS.md`
10. `docs/AI_AGENT_WORKFLOW.md`
11. `docs/DECISIONS.md`

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

1. Read the project status and roadmap.
2. Use the synchronized `project-governance` branch for planning work and `main` as the base for implementation work.
3. Inspect existing implementation before proposing changes.
4. Identify impacted modules and documentation.
5. Keep the change small and reviewable.
6. Prefer existing structure and conventions.
7. Add or update tests when implementation exists.
8. Update affected folder-level `KNOWLEDGE.md` files and the root `KNOWLEDGE.md` map when folder structure changes.
9. Update relevant docs, especially `docs/PROJECT_STATUS.md`, `docs/FUTURE_PROSPECTS.md`, and `docs/DECISIONS.md` when applicable.
10. Summarize changes, tests, and documentation updates.

## Prohibited Without Explicit Approval

- Replacing the selected stack.
- Adding hosted paid dependencies.
- Implementing unrelated features.
- Committing secrets.
- Adding temporary workarounds without documenting the reason.
- Creating deployment pipelines before the approved deployment stage.
