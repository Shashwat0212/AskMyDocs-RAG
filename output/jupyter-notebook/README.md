# Qdrant Billboard Jupyter Tutorial

The notebook is a branch-scoped educational companion. It does not integrate
with the AskMyDocs backend.

## Prepare

From the repository root:

```bash
docker compose -f deployment/compose.qdrant.yaml up -d
uv sync --project sandbox/qdrant_music --extra notebook --extra dev
```

Install the notebook's named kernel:

```bash
uv run --project sandbox/qdrant_music \
  python -m ipykernel install \
  --user \
  --name qdrant-music \
  --display-name "Python (Qdrant Music Tutorial)"
```

This one-time command registers the kernel expected by the committed notebook.
It changes only your local Jupyter kernel registry; the environment itself
remains under `sandbox/qdrant_music/.venv`.

## Open

```bash
uv run --project sandbox/qdrant_music \
  jupyter lab \
  output/jupyter-notebook/qdrant_billboard_internals_tutorial.ipynb
```

Choose `Python (Qdrant Music Tutorial)`, then use **Restart Kernel and Run All
Cells**.

The first embedding cell may download the local Nomic model. Start Qdrant
before running all cells. The notebook uses separate collection names and
idempotent point IDs.

## Safety

- Normal execution does not delete collections or Docker volumes.
- Optional collection cleanup requires `CLEANUP_NOTEBOOK_COLLECTIONS = True`.
- Destructive volume deletion runs only if
  `CONFIRM_DESTRUCTIVE_RESET = True`; automated validation leaves it `False`.
- Canonical outputs are intentionally cleared before commit.

## Automated validation

Execution uses a temporary copy:

```bash
mkdir -p tmp/jupyter-notebook
uv run --project sandbox/qdrant_music \
  jupyter execute \
  output/jupyter-notebook/qdrant_billboard_internals_tutorial.ipynb \
  --output-dir tmp/jupyter-notebook
```

Do not commit the executed copy.
