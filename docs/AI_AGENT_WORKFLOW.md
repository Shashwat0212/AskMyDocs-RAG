# AI Agent Workflow

This workflow keeps Codex, Claude, GitHub Copilot, and future AI coding assistants synchronized.

## Start Of Task

1. Read `AGENTS.md`.
2. Read `docs/PROJECT_STATUS.md`.
3. Read `docs/ROADMAP.md`.
4. Read `docs/ENGINEERING_WORKFLOW.md`.
5. Read `docs/CODING_STANDARDS.md`.
6. Inspect the existing implementation before proposing or making changes.
7. Identify affected docs before editing.

## During Task

- Keep the change focused to the active ticket.
- Follow existing repository structure.
- Prefer configuration over hardcoded values.
- Preserve local-first constraints.
- Avoid unrelated refactors.
- Ask before changing architecture, tooling, or stage order.

## End Of Task

Before reporting completion:

1. Run relevant local checks when implementation exists.
2. Update documentation impacted by the change.
3. Update `docs/PROJECT_STATUS.md` if project status changed.
4. Update `docs/DECISIONS.md` if an architectural, tooling, model, or workflow decision changed.
5. Summarize changed files, tests run, and any follow-up work.

## Agent-Specific Files

- `CLAUDE.md` is a thin Claude adapter.
- `CODEX.md` is a thin Codex adapter.
- `.github/copilot-instructions.md` is a thin GitHub Copilot adapter.

These files must not become competing sources of truth. Project policy belongs in `AGENTS.md` and `docs/`.
