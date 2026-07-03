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
2. `docs/PROJECT_STATUS.md`
3. `docs/ROADMAP.md`
4. `docs/ENGINEERING_WORKFLOW.md`
5. `docs/DEVELOPMENT_ENVIRONMENT.md`
6. `docs/CODING_STANDARDS.md`
7. `docs/AI_AGENT_WORKFLOW.md`
8. `docs/DECISIONS.md`

## Non-Negotiable Project Constraints

- Local-first only.
- Use free and open-source components.
- Do not introduce paid LLM APIs, paid hosted inference, paid vector databases, paid evaluation services, or paid observability platforms.
- Prefer configuration over hardcoded behavior.
- Keep business logic separated from infrastructure concerns.
- Keep changes focused to the assigned ticket.
- Update documentation in the same change as implementation.
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
2. Inspect existing implementation before proposing changes.
3. Identify impacted modules and documentation.
4. Keep the change small and reviewable.
5. Prefer existing structure and conventions.
6. Add or update tests when implementation exists.
7. Update relevant docs, especially `docs/PROJECT_STATUS.md` and `docs/DECISIONS.md` when applicable.
8. Summarize changes, tests, and documentation updates.

## Prohibited Without Explicit Approval

- Replacing the selected stack.
- Adding hosted paid dependencies.
- Implementing unrelated features.
- Committing secrets.
- Adding temporary workarounds without documenting the reason.
- Creating deployment pipelines before the approved deployment stage.
