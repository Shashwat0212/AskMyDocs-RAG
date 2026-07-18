# Engineering Workflow

## Principles

- Every engineer can work on any part of the system.
- Knowledge should be shared continuously.
- Small, independently reviewable changes are preferred.
- Every code change must improve or maintain code quality.
- Documentation evolves alongside implementation.
- Folder-level knowledge docs explain what each part of the repository currently does.
- Configuration should be preferred over hardcoded values.

## Standard Lifecycle

1. Requirement discussion
2. Understand scope and design
3. Create ticket
4. Create feature branch
5. Review existing implementation
6. Implement solution
7. Self-review and local testing
8. Update documentation
9. Create pull request
10. Peer review
11. Address review comments
12. Merge the ticket branch into its epic branch
13. Delete the feature branch
14. Validate the complete epic
15. Merge the epic branch into `main`
16. Delete the epic branch

## Branching

- `main` is the integration branch.
- Create a short-lived epic integration branch from `main` using `epic/<epic-id>-short-description`.
- Create each short-lived ticket branch from the latest active epic branch using `feature/<developer>/<ticket-id>-short-description`.
- Merge ticket pull requests into the epic branch, then merge the validated epic branch into `main`.
- `project-governance` is the permanent planning and project-state branch; do not implement application code on it.

Examples:

- `epic/epic-1-backend-foundations`
- `feature/shashwat/RAG-001-fastapi-sandbox`

## Pull Requests

Every pull request should include:

- Summary of changes
- Related ticket
- Implementation notes
- Testing performed
- Documentation updates
- Knowledge doc updates for affected folders

At least one team member must review every pull request before merge.

Pull requests from `project-governance` to `main` must use a merge commit. Do not squash or rebase them because the permanent branch must retain shared ancestry with `main` for later synchronization.

Ticket pull requests target their active epic branch. Epic pull requests target `main` only after all included ticket work is reviewed and the epic acceptance criteria are validated.

## Jira And Project Tracking

- Jira owns ticket assignment, sprint placement, and workflow state.
- The `project-governance` version of `docs/PROJECT_STATUS.md` provides the live snapshot of the current phase, active epic, blockers, and next work.
- The `main` version of governance documents is the latest approved checkpoint.
- Feature branches and pull requests must reference their Jira ticket. Governance-only updates do not require a placeholder ticket.
- A pull request that changes project state must update `docs/PROJECT_STATUS.md` and any affected plan or decision record.
- Follow `docs/PROJECT_TRACKING.md` for source ownership, status mapping, and synchronization events.

## Review Expectations

Review for:

- Correctness
- Scope control
- Local-first compliance
- Configuration-first behavior
- Error handling
- Meaningful logging
- Test coverage appropriate to the change
- Documentation updates
- Affected folder-level `KNOWLEDGE.md` files

Avoid:

- Duplicate logic
- Large unrelated changes
- Dead code or commented code
- Temporary workarounds without discussion

## Definition Of Done

A ticket is complete only when:

- Acceptance criteria are satisfied.
- Code has been reviewed and approved.
- Required tests pass.
- Documentation is updated.
- Affected folder-level `KNOWLEDGE.md` files are updated.
- The root `KNOWLEDGE.md` map is updated when folders are added, removed, renamed, or repurposed.
- Configuration changes are documented.
- Jira and repository project status are synchronized when the task changes project state.
- Changes are merged into the active epic branch.
- The ticket branch has been deleted after merge.

An epic is delivered only when its integrated ticket work is validated, merged into `main`, and the epic branch is deleted. The permanent `project-governance` branch is retained.

## Knowledge Documentation

Every project-owned folder should contain a `KNOWLEDGE.md` file. These files explain what currently exists in the folder, what the contents do, and which related docs should change when that folder changes.

The repository root `KNOWLEDGE.md` is the knowledge map. It links to each folder-level knowledge doc and summarizes that folder's responsibility.

When implementation changes code, configuration, scripts, documentation structure, or runtime behavior, update the affected folder-level knowledge docs in the same change. When folder structure changes, update the root knowledge map.
