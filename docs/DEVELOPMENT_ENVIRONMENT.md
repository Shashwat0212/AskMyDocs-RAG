# Development Environment

Phase 1 deliberately uses two free execution environments. Epic 1 establishes local foundations. Epics 2 through 6 use free-tier Google Colab as the canonical shared runtime. Epic 7 returns to the local runtime to deliver the Gradio MVP.

## Runtime Matrix

| Phase 1 work | Required environment | Services |
|---|---|---|
| Epic 1 | Developer machine | FastAPI, Docker Compose Qdrant, Ollama |
| Epics 2–5 | Free-tier Colab | Pinned Python environment and ephemeral Qdrant |
| Epic 6 | Free-tier Colab | Pinned Python environment, ephemeral Qdrant, ephemeral Ollama |
| Epic 7 | Developer machine | FastAPI, Docker Compose Qdrant, Ollama, Gradio |

## Local Requirements

- Git
- Docker Desktop or Docker Engine with Docker Compose
- Python 3.11 baseline
- `uv` for Python environment management
- Ollama
- `curl`, `jq`, and Make or an equivalent task runner
- Node.js LTS and `pnpm` for the later final web interface

Use `docs/operations/day_zero_setup.md` for machine setup. Epic 1 adds concrete service commands under its approved tickets.

## Colab Requirements

- Google account with access to free-tier Colab
- Repository read/write access for the assigned branch workflow
- Access to the configured shared Drive artifact root
- Browser permission to mount Drive when required
- Project bootstrap entrypoint introduced by `RAG-005`

Every Colab run must:

1. Start from a fresh runtime and record runtime type, Python version, accelerator availability, and start time.
2. Check out the assigned branch and source commit.
3. Install project-pinned dependencies and capture diagnostics.
4. Mount Drive only for declared datasets and artifacts.
5. Start pinned Qdrant under the Colab runtime filesystem and wait for readiness.
6. Start Ollama only for Epic 6 work that requires generation.
7. Use unique run and collection IDs.
8. Checkpoint long-running manifests/results to Drive and stop cleanly when practical.

Free-tier resource type, accelerator availability, and session duration vary. Workflows must support CPU-compatible fallbacks where practical, checkpointing, resumption, and clear partial/failed run states. Automation is manually launched and end-to-end automated, not unattended scheduling.

Reference: [Google Colab FAQ](https://research.google.com/colaboratory/faq.html).

## Persistence Boundary

- **Git:** reviewed package code, thin notebooks, configuration schemas, selected profiles, compact fixtures, manifests, and summary reports.
- **Shared Drive:** datasets, query/relevance assets when too large for Git, checkpoints, and full experiment artifacts.
- **Colab runtime filesystem:** Qdrant storage, temporary extraction/index files, downloaded model caches, logs being processed, and other disposable working state.
- **Local runtime:** Docker volumes and model caches used for Epic 1 validation and Epic 7 rehydration.

Never configure Colab Qdrant storage under `/content/drive` or another mounted Drive path. Never place secrets in notebooks, config files, Qdrant payloads, reports, or Git.

## Models And Retrieval Components

- Generation baseline: `qwen3:4b`
- Dense embedding baseline: `nomic-embed-text-v1.5`, subject to Epic 5 evidence
- Sparse retrieval baseline: Qdrant BM25/sparse vectors
- Fusion baseline: Qdrant Query API RRF; DBSF configurable
- Initial reranker: `cross-encoder/ms-marco-MiniLM-L-6-v2`
- Quality/critic and alternative embedding/reranking models remain future or experiment-profile choices unless explicitly approved

## Environment Variables

Use `.env.example` as the shared variable-name reference. Do not commit `.env` files. Runtime configuration should cover application/logging, Qdrant and Ollama endpoints, model/config paths, collection prefixes, Qdrant runtime storage, Drive artifact root, and profile/manifest locations.

## Package And Command Conventions

- Prefer `uv` and the committed lock or equivalent pinned dependency mechanism once introduced by an approved ticket.
- Colab and local runtimes must install the same project package rather than maintain separate implementations.
- Common commands should be exposed through Make or an equivalent task runner as tickets add them.
- Do not install dependencies, models, or services before the ticket that owns them.
