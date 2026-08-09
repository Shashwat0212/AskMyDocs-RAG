# Coding Standards

These standards govern implementation handoffs even though this branch contains no application code.

## Architecture

- Keep domain and business logic in importable packages.
- Keep FastAPI routes, Qdrant clients, Ollama clients, Colab launchers, and UI code as adapters around that logic.
- Use typed configuration and stable interfaces.
- Do not hide configuration choices in notebooks or route handlers.
- Carry one `trace_id` through a complete user workflow.

## Quality

- Add focused tests for new behavior and expected failures.
- Keep deterministic IDs, seeds, profile versions, and run manifests reproducible.
- Fail clearly on profile, model, dimension, payload, or collection incompatibility.
- Use structured logs without document content, prompts, secrets, or personal data.
- Keep generated and large runtime artifacts out of Git unless a ticket explicitly approves a compact fixture or summary.

## Retrieval And Evaluation

- Keep ingestion/index settings separate from query-time settings.
- Never let the query navigator select a setting that requires rebuilding the collection.
- Use stable source evidence rather than profile-dependent chunk IDs as golden truth.
- Keep development and locked-holdout benchmark data separated.
- Record every profile and tree version in traces and reports.
- Prefer deterministic retrieval metrics for Phase 1; do not treat LLM opinion as retrieval ground truth.

## Security And Dependencies

- Use free/open-source dependencies with compatible licenses.
- Do not add paid APIs, hosted inference, hosted vector databases, paid evaluation, or paid observability.
- Never commit secrets, tokens, private documents, model weights, or confidential benchmark data.
