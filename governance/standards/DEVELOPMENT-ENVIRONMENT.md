# Development Environment

## Runtime By Epic

| Epic | Runtime |
|---|---|
| 1 | Local FastAPI, Docker Qdrant, and Ollama |
| 2–6 | Free-tier Colab with pinned dependencies and self-managed services |
| 7 | Local FastAPI, Docker Qdrant, Ollama, and Gradio |

## Colab Rules

- Bootstrap from the assigned implementation branch.
- Pin dependencies and record runtime diagnostics.
- Keep Qdrant storage on the runtime filesystem, never mounted Drive.
- Mount Drive only for declared datasets, checkpoints, and full artifacts.
- Make long evaluation and experiment runs checkpointed, resumable, and failure-isolated.
- Record interrupted or resource-limited 100-million-token runs honestly.
- Do not rely on notebook-only business logic.

## Local Rules

- Use Docker Compose for approved local services.
- Keep service versions pinned.
- Document readiness, logs, normal shutdown, persistence, and destructive reset separately.
- Rebuild selected Epic 5 profiles locally before declaring the MVP complete.

## Durable Records

Git may contain reviewed code, compact public fixtures, schema examples, profile definitions, run manifests, and summary reports. Shared Drive may contain source datasets, full golden records when too large for Git, checkpoints, embeddings, and complete experiment outputs.

Never place secrets, confidential documents, live Qdrant storage, or unreviewed sensitive data in Git or shared Drive.
