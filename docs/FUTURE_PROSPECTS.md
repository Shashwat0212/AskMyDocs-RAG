# Future Prospects

## Purpose

This register captures possible future project directions explored during planning. A prospect is not an approved commitment until its status is `Approved` and the resulting roadmap, architecture, and decision changes are merged into `main`.

## Statuses

- `Exploring`: early investigation with material unknowns.
- `Proposed`: sufficiently defined for project-owner review.
- `Approved`: accepted and promoted into the roadmap or an architecture plan.
- `Deferred`: valid direction intentionally postponed.
- `Rejected`: considered and intentionally not pursued.

## Current Prospects

No unapproved prospects are currently recorded. Phase 1 Epics 7 through 9 are already approved planning items and remain in `docs/architecture/phase_1_core_rag_mvp.md`.

## Entry Template

Copy this section for each new prospect and replace `PROSPECT-NNN` with the next sequential identifier.

```text
ID: PROSPECT-NNN
Title:
Status: Exploring | Proposed | Approved | Deferred | Rejected
Target Stage Or Epic:
Last Reviewed: YYYY-MM-DD
Rationale:
Proposed Direction:
Dependencies:
Risks:
Evidence:
Resulting Decision:
```

## Promotion Rule

When a prospect becomes `Approved`:

1. Update its status and last-reviewed date.
2. Update `docs/ROADMAP.md` or the relevant file under `docs/architecture/`.
3. Add an active entry to `docs/DECISIONS.md` when the approval changes architecture, tooling, models, workflow, or repository conventions.
4. Link the resulting decision from the prospect.
5. Merge the governance checkpoint into `main` before implementation starts.

Rejected and deferred prospects remain in this file so the reasoning is not lost.
