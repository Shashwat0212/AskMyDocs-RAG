# AI Agent Workflow

This workflow keeps Codex, Claude, GitHub Copilot, and future AI coding assistants synchronized.

## Start Of Task

1. Read `starter.md`.
2. Read `AGENTS.md`.
3. Use the task-routing table in `starter.md` to load the relevant detailed sources.
4. Read both governing DOCX files before changing architecture, roadmap direction, selected stack, project constraints, or stage ordering.
5. Inspect the existing implementation before proposing or making changes.
6. Identify affected docs and folder-level knowledge docs before editing.

Planning and future-epic tasks should run on the synchronized `project-governance` branch. Approved epic integration branches start from `main`, which contains the latest approved governance checkpoint. Ticket implementation branches start from the latest active epic branch.

## During Task

- Keep the change focused to the active ticket.
- Follow existing repository structure.
- Prefer configuration over hardcoded values.
- Preserve local-first constraints.
- Avoid unrelated refactors.
- Ask before changing architecture, tooling, or stage order.
- Record tentative future directions in `docs/FUTURE_PROSPECTS.md`; do not present them as accepted decisions.
- Update affected folder-level `KNOWLEDGE.md` files when changing code, configuration, scripts, documentation structure, or behavior.
- Update the root `KNOWLEDGE.md` map when folders are added, removed, renamed, or repurposed.

## End Of Task

Before reporting completion:

1. Run relevant local checks when implementation exists.
2. Update documentation impacted by the change.
3. Update affected folder-level `KNOWLEDGE.md` files.
4. Update the root `KNOWLEDGE.md` map if folder structure changed.
5. Update `docs/PROJECT_STATUS.md` if project status changed.
6. Update `docs/DECISIONS.md` if an architectural, tooling, model, or workflow decision changed.
7. Update `docs/FUTURE_PROSPECTS.md` if exploratory planning changed.
8. Update `starter.md` if its current-state summary changed.
9. Confirm Jira and repository tracking are synchronized when project state changed.
10. Synchronize `main` and `project-governance` according to `docs/PROJECT_TRACKING.md` when the task changes approved guidance or implemented state.
11. Summarize changed files, tests run, and any follow-up work.

## Agent-Specific Files

- `CLAUDE.md` is a thin Claude adapter.
- `CODEX.md` is a thin Codex adapter.
- `.github/copilot-instructions.md` is a thin GitHub Copilot adapter.

These files must not become competing sources of truth. Project policy belongs in `AGENTS.md` and `docs/`.
