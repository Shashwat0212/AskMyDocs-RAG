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
