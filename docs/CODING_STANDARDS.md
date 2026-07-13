# Coding Standards

## General Standards

- Keep changes focused to the assigned ticket.
- Write modular and reusable code.
- Separate business logic from infrastructure concerns.
- Prefer configuration over hardcoded values.
- Add meaningful logging.
- Handle expected error scenarios.
- Maintain consistent project structure and coding standards.
- Avoid duplicate logic.
- Avoid dead code and commented-out code.

## Local-First Rule

Do not introduce paid hosted services or paid APIs. All model serving, vector storage, evaluation, and observability choices must preserve the local-first architecture unless the project owner explicitly approves a change.

## Configuration

Runtime behavior should be driven by configuration files and environment variables where appropriate. Do not bury model names, collection names, thresholds, prompt versions, or service URLs directly in feature code.

## Documentation

Update documentation whenever implementation changes. This includes:

- Architecture documentation
- API documentation
- Configuration documentation
- Feature documentation
- Operational or deployment documentation
- Affected folder-level `KNOWLEDGE.md` files
- Project status
- Decision log when architecture or workflow changes

## Testing

Tests should scale with risk:

- Unit tests for isolated logic
- Integration tests for service boundaries
- Regression tests for retrieval and evaluation behavior once those stages exist

Do not mark a task complete until required local checks pass or the reason they could not be run is documented.

## Scope Control

Do not implement future-stage behavior during earlier-stage tickets unless explicitly approved. The roadmap order matters.
