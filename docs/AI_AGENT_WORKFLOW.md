# AI Agent Workflow

This workflow keeps Codex, Claude, GitHub Copilot, and future AI coding assistants synchronized.

## Start Of Task

1. Read `AGENTS.md`.
2. Read `KNOWLEDGE.md`.
3. Read `docs/PROJECT_STATUS.md`.
4. Read `docs/PROJECT_TRACKING.md`.
5. Read `docs/FUTURE_PROSPECTS.md` for planning and future-epic work.
6. Read `docs/ROADMAP.md`.
7. Read `docs/ENGINEERING_WORKFLOW.md`.
8. Read `docs/CODING_STANDARDS.md`.
9. Inspect the existing implementation before proposing or making changes.
10. Identify affected docs and folder-level knowledge docs before editing.

Planning and future-epic tasks should run on the synchronized `project-governance` branch. Implementation tasks should start from `main`, which contains the latest approved governance checkpoint.

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
8. Confirm Jira and repository tracking are synchronized when project state changed.
9. Synchronize `main` and `project-governance` according to `docs/PROJECT_TRACKING.md` when the task changes approved guidance or implemented state.
10. Summarize changed files, tests run, and any follow-up work.

## Agent-Specific Files

- `CLAUDE.md` is a thin Claude adapter.
- `CODEX.md` is a thin Codex adapter.
- `.github/copilot-instructions.md` is a thin GitHub Copilot adapter.

These files must not become competing sources of truth. Project policy belongs in `AGENTS.md` and `docs/`.
