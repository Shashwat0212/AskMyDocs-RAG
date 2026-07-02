# Engineering Workflow

## Principles

- Every engineer can work on any part of the system.
- Knowledge should be shared continuously.
- Small, independently reviewable changes are preferred.
- Every code change must improve or maintain code quality.
- Documentation evolves alongside implementation.
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

At least one team member must review every pull request before merge.

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
- Configuration changes are documented.
- Changes are merged into `main`.
- The feature branch has been deleted.
