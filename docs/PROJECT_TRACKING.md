# Project Tracking

## Purpose

This document defines how Jira work items and repository planning documents stay synchronized. It does not replace Jira or duplicate every ticket field in the repository.

## Sources Of Truth

| Information | Source of truth | Repository responsibility |
|---|---|---|
| Ticket assignee, workflow state, sprint, and day-to-day execution | Jira | Link the ticket from its branch and pull request. |
| Current phase, active epic, blockers, and near-term sequence | `docs/PROJECT_STATUS.md` | Keep a concise snapshot aligned with Jira. |
| Stage ordering and product direction | `docs/ROADMAP.md` | Update only when approved scope or sequencing changes. |
| Epic scope and representative ticket breakdown | `docs/architecture/` | Keep acceptance boundaries and dependencies explicit. |
| Architecture, tooling, model, workflow, and repository decisions | `docs/DECISIONS.md` | Record durable decisions and their consequences. |
| Governing project intent | `docs/source_documents/` | Do not override without project-owner approval. |

## Branch Policy

Project tracking and decision documents live on `main` with the implementation they describe. Update them through short-lived ticket branches and pull requests. Do not maintain a permanent planning or tracking branch because it would drift from the code and create a competing project state.

The initial governance setup uses `feature/RAG-000-project-governance`. After it is reviewed and merged, future tickets update the tracking documents in their own branches when project state changes.

## Status Vocabulary

- `Planned`: scoped in repository planning but not started.
- `Ready`: approved and available to start.
- `In Progress`: actively being worked.
- `Blocked`: unable to progress, with the blocker recorded.
- `Done`: acceptance criteria are met and the pull request is merged into `main`.

Jira may use different display names, but the meaning should map to these states in `docs/PROJECT_STATUS.md`.

## Synchronization Rules

Update project tracking when any of these events occurs:

1. A ticket or epic is created, renamed, split, merged, reprioritized, or materially rescoped.
2. Work starts, becomes blocked, is unblocked, or is completed.
3. A pull request changes the roadmap, architecture, workflow, tooling, model selection, or repository conventions.
4. A merge changes the current phase, active epic, next ticket, or known blockers.

For each relevant change:

1. Update the Jira ticket state and link the branch or pull request.
2. Update `docs/PROJECT_STATUS.md` if the current snapshot changed.
3. Update the relevant roadmap or architecture plan if scope or sequence changed.
4. Add a `docs/DECISIONS.md` entry when a durable decision changed.
5. Update affected `KNOWLEDGE.md` files.

## Review Cadence

Review `docs/PROJECT_STATUS.md` at epic planning, sprint planning, and before merging any ticket that changes project state. The status file must include a last-updated date so stale snapshots are visible.
