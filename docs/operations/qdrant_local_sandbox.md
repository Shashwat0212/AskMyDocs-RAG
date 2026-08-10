# Qdrant Local Sandbox Operations

This runbook covers the isolated RAG-002 Qdrant service. It is not a production
deployment guide.

## Paths and ports

- Compose file: `deployment/compose.qdrant.yaml`
- REST and dashboard: `http://localhost:6333`
- gRPC: `localhost:6334`
- Readiness: `http://localhost:6333/readyz`
- Named volume: `askmydocs_qdrant_sandbox_data`

Both ports bind to `127.0.0.1`.

## Start and verify

```bash
docker compose -f deployment/compose.qdrant.yaml config
docker compose -f deployment/compose.qdrant.yaml up -d
docker compose -f deployment/compose.qdrant.yaml ps
uv run --project sandbox/qdrant_music qdrant-music wait-ready
curl http://localhost:6333/readyz
```

## Logs and inspection

```bash
docker compose -f deployment/compose.qdrant.yaml logs -f qdrant
curl http://localhost:6333/collections
curl http://localhost:6333/telemetry
curl http://localhost:6333/metrics
uv run --project sandbox/qdrant_music \
  qdrant-music collection inspect --kind baseline
```

Qdrant Web UI is available at `http://localhost:6333/dashboard`.

## Stop while preserving data

```bash
docker compose -f deployment/compose.qdrant.yaml down
```

The named volume remains. Restart and run the persistence check:

```bash
docker compose -f deployment/compose.qdrant.yaml up -d
uv run --project sandbox/qdrant_music qdrant-music wait-ready
uv run --project sandbox/qdrant_music \
  python -m qdrant_music.tutorial_steps.q15_persistence
```

## Collection-only cleanup

```bash
uv run --project sandbox/qdrant_music \
  qdrant-music collection delete --kind baseline
uv run --project sandbox/qdrant_music \
  qdrant-music collection delete --kind hnsw
```

This preserves the Docker volume and other collections.

## Destructive reset

> **Warning:** this permanently deletes every collection in the sandbox volume.

```bash
docker compose -f deployment/compose.qdrant.yaml down --volumes
```

Confirm removal:

```bash
docker volume inspect askmydocs_qdrant_sandbox_data
```

The inspect command should report that the volume does not exist.

## Troubleshooting

### Port 6333 is already in use

Find the existing listener and stop the conflicting local service. Do not
silently change the shared tutorial port because every learning path uses the
same setting.

### Qdrant is running but Python cannot connect

```bash
curl -v http://localhost:6333/readyz
docker compose -f deployment/compose.qdrant.yaml logs --tail=100 qdrant
```

Verify that `QDRANT_URL`, if set, is `http://localhost:6333`.

### Collection schema mismatch

The tutorial refuses to overwrite a collection with an unexpected vector size
or metric. Delete only the named tutorial collection with the CLI, then create
it again.

### HNSW index timeout

Inspect collection and logs. The learning collection deliberately uses low
thresholds, but index construction is asynchronous:

```bash
uv run --project sandbox/qdrant_music \
  qdrant-music collection inspect --kind hnsw
docker compose -f deployment/compose.qdrant.yaml logs --tail=100 qdrant
```

### Model is unavailable

The first FastEmbed use downloads the model. Restore network access for initial
provisioning, then rerun Q04. No hosted inference is used.
