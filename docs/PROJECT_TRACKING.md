# Project Tracking

## Purpose

This document defines how the permanent `project-governance` branch, Jira work items, and approved repository documentation stay synchronized.

`project-governance` is the visible working view of project status, future prospects, planning changes, and proposed decisions. `main` remains the approved implementation baseline. Governance changes must be merged into `main` before they direct implementation.

## Sources Of Truth

| Information | Source of truth | Repository responsibility |
|---|---|---|
| Start-of-run orientation | `starter.md` | Summarize current approved and working context without replacing detailed sources. |
| Ticket assignee, sprint, workflow state, and day-to-day execution | Jira | Record ticket keys, links, and summary status manually. |
| Current phase, active epic, blockers, and near-term sequence | `project-governance` version of `docs/PROJECT_STATUS.md` | Keep the live project snapshot current. |
| Exploratory future ideas | `project-governance` version of `docs/FUTURE_PROSPECTS.md` | Keep unapproved possibilities separate from commitments. |
| Approved stage ordering and product direction | `main` version of `docs/ROADMAP.md` | Merge approved governance checkpoints before implementation. |
| Approved epic scope and ticket breakdown | `main` version of `docs/architecture/` | Keep acceptance boundaries and dependencies explicit. |
| Accepted architecture, tooling, model, workflow, and repository decisions | `main` version of `docs/DECISIONS.md` | Preserve active and superseded decision history. |
| Governing project intent | `docs/source_documents/` | Do not override without project-owner approval. |

## Branch Policy

- `main` is the approved implementation baseline and the base for epic integration branches.
- `project-governance` is a permanent planning and project-state branch.
- Epic integration branches start from `main`, use `epic/<epic-id>-short-description`, collect reviewed ticket work, and merge into `main` when the epic is validated.
- Ticket branches start from the latest active epic branch, use `feature/<developer>/<ticket-id>-short-description`, and merge back into that epic branch.
- `project-governance` is the only permanent non-main branch; epic and ticket branches are deleted after their integration work is merged.
- Governance work does not require a placeholder Jira ticket. Reference a Jira ticket when the update relates to one.
- Do not implement application code on `project-governance`.

## Two-Way Synchronization

### Before Planning

Bring completed implementation and approved documentation into the governance branch:

```bash
git switch project-governance
git fetch origin
git merge origin/main
```

Resolve any documentation conflicts in favor of the actual implemented state, then update the project snapshot or plans.

### Approving Governance Changes

When a prospect, plan, or decision is approved:

1. Update the relevant roadmap or architecture plan.
2. Add or update the decision record.
3. Update project status and affected `KNOWLEDGE.md` files.
4. Open a pull request from `project-governance` to `main`.
5. Merge with a merge commit. Do not squash or rebase this pull request because the permanent branch requires shared ancestry for repeated synchronization.

### After An Approved Governance Merge

Bring the merge commit back into the permanent branch:

```bash
git switch project-governance
git fetch origin
git merge origin/main
git push origin project-governance
```

### After Epic Work

After a ticket pull request merges into an epic branch, update Jira and the live project status as needed. After the validated epic branch merges into `main`, merge `main` into `project-governance`, then update `docs/PROJECT_STATUS.md`, Jira links, blockers, completed work, and affected plans. If those updates change approved guidance, merge the next governance checkpoint back into `main`.

## Status Vocabulary

Ticket summaries use these repository states:

- `Planned`: scoped but not approved to start.
- `Ready`: approved and available to start.
- `In Progress`: actively being worked.
- `Blocked`: unable to progress, with the blocker recorded.
- `Done`: ticket acceptance criteria are met and the ticket pull request is merged into its active epic branch. Epic delivery is complete only after the validated epic branch is merged into `main`.

Jira may use different display names, but its workflow states should map to these meanings in `docs/PROJECT_STATUS.md`.

Future prospects use `Exploring`, `Proposed`, `Approved`, `Deferred`, or `Rejected` as defined in `docs/FUTURE_PROSPECTS.md`.

## Update Events

Update governance records when any of these events occurs:

1. A planning session creates or materially changes a future prospect.
2. A ticket or epic is created, renamed, split, merged, reprioritized, or rescoped.
3. Work starts, becomes blocked, is unblocked, or is completed.
4. A change affects the roadmap, architecture, workflow, tooling, model selection, or repository conventions.
5. A merge changes the current phase, active epic, next ticket, or known blockers.
6. The approved stack, implemented repository shape, branch policy, or a major summarized decision changes.

When one of these events makes the orientation snapshot stale, update `starter.md` in the same governance change.

## Review Cadence

Review the governance branch before epic planning, sprint planning, and implementation based on a new decision. Update `docs/PROJECT_STATUS.md` after every merge that changes project state. Every live snapshot and future prospect must include a last-reviewed date so stale information is visible.

## Jira Synchronization

Jira synchronization is manual in the first version. Store only ticket keys, links, and summary states in Markdown. Do not add Jira credentials, API tokens, synchronization scripts, or hosted automation as part of this governance setup.
