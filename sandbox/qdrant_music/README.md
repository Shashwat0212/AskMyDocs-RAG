# Qdrant Billboard Music Sandbox

This is an isolated, local-first learning project for RAG-002. It deliberately
does not integrate with the AskMyDocs backend.

## Quick start

From the repository root:

```bash
docker compose -f deployment/compose.qdrant.yaml up -d
uv sync --project sandbox/qdrant_music --extra dev --extra notebook
uv run --project sandbox/qdrant_music qdrant-music wait-ready
uv run --project sandbox/qdrant_music qdrant-music dataset validate
uv run --project sandbox/qdrant_music qdrant-music collection create --kind baseline
uv run --project sandbox/qdrant_music qdrant-music collection load --kind baseline
uv run --project sandbox/qdrant_music qdrant-music search \
  --query "uplifting energetic pop with a strong dance feel"
```

Read `docs/tutorials/qdrant_billboard_walkthrough.md` before working through the
numbered programs. Operational commands and troubleshooting live in
`docs/operations/qdrant_local_sandbox.md`.

## First model download

FastEmbed downloads `nomic-ai/nomic-embed-text-v1.5` on first use. The model is
Apache-2.0 licensed and runs locally after it is cached.
