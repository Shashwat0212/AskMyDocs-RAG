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
12. Merge into `main`
13. Delete feature branch

## Branching

- `main` is the integration branch.
- Use short-lived feature branches.
- Keep project status, plans, and decisions on `main`; do not use a permanent tracking branch.
- Branch naming: `feature/<ticket-id>-short-description`

Examples:

- `feature/RAG-001-backend-foundation`
- `feature/RAG-014-retrieval-trace-view`

## Pull Requests

Every pull request should include:

- Summary of changes
- Related ticket
- Implementation notes
- Testing performed
- Documentation updates
- Knowledge doc updates for affected folders

At least one team member must review every pull request before merge.

## Jira And Project Tracking

- Jira owns ticket assignment, sprint placement, and workflow state.
- `docs/PROJECT_STATUS.md` provides the repository snapshot of the current phase, active epic, blockers, and next work.
- Branches and pull requests must reference their Jira ticket.
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

A task is complete only when:

- Acceptance criteria are satisfied.
- Code has been reviewed and approved.
- Required tests pass.
- Documentation is updated.
- Affected folder-level `KNOWLEDGE.md` files are updated.
- The root `KNOWLEDGE.md` map is updated when folders are added, removed, renamed, or repurposed.
- Configuration changes are documented.
- Jira and repository project status are synchronized when the task changes project state.
- Changes are merged into `main`.
- The feature branch has been deleted.

## Knowledge Documentation

Every project-owned folder should contain a `KNOWLEDGE.md` file. These files explain what currently exists in the folder, what the contents do, and which related docs should change when that folder changes.

The repository root `KNOWLEDGE.md` is the knowledge map. It links to each folder-level knowledge doc and summarizes that folder's responsibility.

When implementation changes code, configuration, scripts, documentation structure, or runtime behavior, update the affected folder-level knowledge docs in the same change. When folder structure changes, update the root knowledge map.
