# Project Tracking And Promotion

## Sources Of Truth

| Information | Source |
|---|---|
| Current phase, blockers, and next work | `governance/current/STATUS.md` |
| Roadmap and epic order | `governance/roadmap/ROADMAP.md` |
| Detailed Phase 1 scope | `governance/phase-1/` |
| Accepted and superseded choices | `governance/decisions/DECISIONS.md` |
| Ticket assignment, sprint, state, and URL | Jira |
| Implemented product state | `main` and the active epic branch |
| Original owner intent | `governance/sources/` |

## Branch Roles

- `project-governance` is a permanent, documentation-only planning branch.
- `main` is the approved implementation baseline.
- Epic branches start from `main`, collect ticket work, and merge into `main` after validation.
- Ticket branches start from the latest active epic branch and target that branch in pull requests.
- `project-governance` is never merged wholesale into `main`, and `main` is not merged into `project-governance`.

## Promoting An Approved Plan

1. Approve the change in the roadmap, epic file, and decision log.
2. Create a handoff record with:
   - Governance commit SHA.
   - Target epic and ticket identifiers.
   - Target implementation branch.
   - Approved scope and acceptance criteria.
   - Exact governance documents to consult or copy.
3. Copy only the implementation-facing guidance into the target epic branch.
4. Do not copy the governance branch structure, branch-only deletions, status history, or exploratory prospects.
5. Record the implementation commit or pull request in `governance/handoffs/PROMOTION-LOG.md`.

Prefer copying a focused handoff document over cherry-picking a broad governance commit.

## Recording Implementation Progress

After ticket or epic work changes implementation state:

1. Read Jira and the relevant implementation branch or `main`.
2. Update `STATUS.md` with the actual state and commit reference.
3. Update the promotion log when a handoff has been implemented.
4. Update the roadmap or epic file only when scope or sequencing changes.
5. Add a decision only for architecture, tooling, model, workflow, or repository-policy changes.

Do not merge implementation history into this branch.

## Status Vocabulary

- `Planned`: scoped but not approved to start.
- `Ready`: approved and available to start.
- `In Progress`: active implementation.
- `Blocked`: unable to progress, with the blocker recorded.
- `Done`: acceptance criteria met and merged into the active epic branch.

An epic is delivered only after its integrated work is validated and merged into `main`.

## Review Events

Review governance when:

- An epic or ticket is added, renumbered, split, merged, or rescoped.
- Work starts, finishes, or becomes blocked.
- Runtime, architecture, tooling, models, or constraints change.
- A prospect is approved, deferred, rejected, or promoted.
- An implementation merge changes the current phase or next work.

Jira synchronization remains manual. Never store Jira credentials or API tokens in this branch.
