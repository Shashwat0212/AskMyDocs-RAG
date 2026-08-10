# Deployment

This folder contains `compose.qdrant.yaml`, the first approved local service
orchestration asset. It runs the pinned Qdrant 1.18.2 RAG-002 learning service.

```bash
docker compose -f deployment/compose.qdrant.yaml up -d
```

REST (`6333`) and gRPC (`6334`) bind to loopback. Collections persist in the
named `askmydocs_qdrant_sandbox_data` volume.

Read `docs/tutorials/qdrant_billboard_walkthrough.md` for the guided lab and
`docs/operations/qdrant_local_sandbox.md` for operations and reset commands.
Production orchestration and deployment pipelines remain future work.
