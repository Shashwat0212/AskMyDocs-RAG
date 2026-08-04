# GitHub Copilot Instructions

Read `starter.md` first and use `AGENTS.md` as the canonical repository instruction file. Load the task-specific sources selected by the routing table in `starter.md` before accepting changes.

Copilot-generated suggestions must follow these project rules:

- Follow the phase-specific runtime model: Epic 1 and 7 local, Epics 2–6 free-tier Colab.
- Free and open-source components only.
- Keep Qdrant/Ollama self-managed, Colab Qdrant storage off Drive, and notebooks thin.
- Configuration over hardcoded values.
- No feature implementation outside the active ticket.
- Documentation updates are required when behavior, architecture, configuration, or workflow changes.

Before accepting generated code, confirm it aligns with `docs/CODING_STANDARDS.md`, `docs/ENGINEERING_WORKFLOW.md`, and `docs/ROADMAP.md`.
