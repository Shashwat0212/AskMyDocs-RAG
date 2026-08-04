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

## Runtime And Free-Software Rule

Epic 1 and Epic 7 run locally; Epics 2–6 run canonically in free-tier Colab. Free Colab is the only approved hosted-compute exception. Do not introduce paid APIs, paid hosted inference, hosted vector databases, paid evaluation, paid observability, or paid experiment tracking. Qdrant and Ollama remain self-managed.

Keep business logic in importable packages, not notebooks or infrastructure adapters. During Colab runs, Qdrant storage must stay on the runtime filesystem. Persist datasets and full artifacts to configured Drive storage and reviewed compact artifacts to Git.

## Configuration

Runtime behavior should be driven by configuration files and environment variables where appropriate. Do not bury model names, collection names, vector names, dimensions, thresholds, fusion, reranking bounds, prompt versions, service URLs, or artifact locations directly in feature code. Preserve the ingestion/index profile, query profile, and run-manifest contracts.

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

Do not mark a task complete until required checks pass in the canonical epic runtime or the environmental limitation and safe follow-up are documented.

## Scope Control

Do not implement future-stage behavior during earlier-stage tickets unless explicitly approved. The roadmap order matters.
