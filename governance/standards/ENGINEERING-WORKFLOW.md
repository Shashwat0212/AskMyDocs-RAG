# Engineering Workflow

## Principles

- Work from an approved ticket and keep changes reviewable.
- Prefer configuration over hardcoded behavior.
- Keep business logic separate from infrastructure and notebooks.
- Use free/open-source, local-first components.
- Update tests and implementation documentation with behavior changes.
- Record runtime versions, data boundaries, and reproducibility inputs.

## Implementation Lifecycle

1. Approve scope through governance and Jira.
2. Promote a focused handoff to the target epic branch.
3. Create the ticket branch from the latest epic branch.
4. Inspect the existing implementation and affected documentation.
5. Implement the ticket only.
6. Test in the epic’s canonical runtime.
7. Update documentation and affected implementation `KNOWLEDGE.md` files.
8. Open a pull request into the epic branch.
9. Review, address comments, merge, and delete the ticket branch.
10. Validate the integrated epic, merge it into `main`, and delete the epic branch.
11. Record completion and implementation references in governance.

## Branches

- `project-governance`: permanent documentation-only planning branch; never merged wholesale into `main`.
- `main`: approved implementation baseline.
- `epic/<epic-id>-short-description`: short-lived integration branch from `main`.
- `feature/<developer>/<ticket-id>-short-description`: short-lived ticket branch from the active epic branch.

Do not implement application code on `project-governance`. Do not copy its branch-only deletions or information architecture into an implementation branch.

## Runtime And Artifacts

- Epic 1 runs locally.
- Epics 2–6 run canonically in free-tier Colab.
- Epic 7 runs locally.
- Qdrant data in Colab stays on the runtime filesystem.
- Shared Drive stores declared datasets, checkpoints, and full experiment artifacts.
- Git stores reviewed code, compact fixtures, manifests, selected profiles, and summaries.
- Notebooks remain thin launchers over importable package code.

## Pull Requests

Every implementation pull request includes:

- Summary and related ticket.
- Implementation notes.
- Tests and runtime used.
- Documentation and configuration updates.
- Relevant artifact or benchmark references.

Ticket pull requests target the active epic branch. Epic pull requests target `main` only after integrated validation.

## Definition Of Done

A ticket is done when its acceptance criteria pass, tests and documentation are updated, no secrets or unintended artifacts are committed, and the reviewed change is merged into the active epic branch.

An epic is done when its tickets work together in the canonical runtime, the epic acceptance criteria pass, the integration branch is merged into `main`, and governance records the result.
