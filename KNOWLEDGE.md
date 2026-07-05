# Repository Knowledge Map

This file maps the folder-level knowledge documents in this repository. Each folder that contains project-owned files should have a `KNOWLEDGE.md` file explaining what the folder contains, what the code or documents do, and which related documentation must be updated when that folder changes.

Knowledge docs complement README files:

- `README.md` explains how to approach or use an area.
- `KNOWLEDGE.md` explains what currently exists in that area and how it fits into the system.

## Update Rule

When a change modifies code, configuration, scripts, documentation structure, or behavior in a folder, update that folder's `KNOWLEDGE.md` in the same change. If the change adds, removes, renames, or repurposes a folder, update this root map as well.

## Folder Map

| Folder | Knowledge doc | Current responsibility |
|---|---|---|
| `.github/` | [.github/KNOWLEDGE.md](.github/KNOWLEDGE.md) | GitHub collaboration metadata and PR guidance. |
| `backend/` | [backend/KNOWLEDGE.md](backend/KNOWLEDGE.md) | Future FastAPI backend boundary. |
| `configs/` | [configs/KNOWLEDGE.md](configs/KNOWLEDGE.md) | Example configuration files for future local-first runtime settings. |
| `deployment/` | [deployment/KNOWLEDGE.md](deployment/KNOWLEDGE.md) | Future local deployment and service orchestration documentation. |
| `docs/` | [docs/KNOWLEDGE.md](docs/KNOWLEDGE.md) | Project documentation, status, workflow, architecture, and decisions. |
| `docs/api/` | [docs/api/KNOWLEDGE.md](docs/api/KNOWLEDGE.md) | Future FastAPI route and API contract documentation. |
| `docs/architecture/` | [docs/architecture/KNOWLEDGE.md](docs/architecture/KNOWLEDGE.md) | Architecture plans, module boundaries, and staged implementation notes. |
| `docs/evaluation_reports/` | [docs/evaluation_reports/KNOWLEDGE.md](docs/evaluation_reports/KNOWLEDGE.md) | Future static evaluation report outputs. |
| `docs/operations/` | [docs/operations/KNOWLEDGE.md](docs/operations/KNOWLEDGE.md) | Local setup, operations, and troubleshooting documentation. |
| `docs/source_documents/` | [docs/source_documents/KNOWLEDGE.md](docs/source_documents/KNOWLEDGE.md) | Owner-provided source-of-truth planning documents. |
| `evals/` | [evals/KNOWLEDGE.md](evals/KNOWLEDGE.md) | Future evaluation assets and regression test organization. |
| `evals/datasets/` | [evals/datasets/KNOWLEDGE.md](evals/datasets/KNOWLEDGE.md) | Future evaluation datasets. |
| `evals/regression_tests/` | [evals/regression_tests/KNOWLEDGE.md](evals/regression_tests/KNOWLEDGE.md) | Future RAG regression test definitions. |
| `evals/reports/` | [evals/reports/KNOWLEDGE.md](evals/reports/KNOWLEDGE.md) | Future generated evaluation reports. |
| `frontend/` | [frontend/KNOWLEDGE.md](frontend/KNOWLEDGE.md) | Frontend application boundaries. |
| `frontend/gradio_app/` | [frontend/gradio_app/KNOWLEDGE.md](frontend/gradio_app/KNOWLEDGE.md) | Future Stage 1 Gradio MVP interface. |
| `frontend/web_app/` | [frontend/web_app/KNOWLEDGE.md](frontend/web_app/KNOWLEDGE.md) | Future React / Next.js interface. |
| `scripts/` | [scripts/KNOWLEDGE.md](scripts/KNOWLEDGE.md) | Local setup and repository utility scripts. |

