# Qdrant Internals Through Billboard Song Search

Ticket: `RAG-002`
Audience: developers who can read basic Python but are new to vector databases
Runtime: local Docker Compose, Python 3.11, `uv`, Qdrant 1.18.2
Time: approximately 90–120 minutes

This is a guided lab, not product code. You will build a semantic song finder
over a frozen Billboard Hot 100 top-50 snapshot, then inspect what Qdrant does
below the client API. The narrow local embedding helper exists only to give the
Qdrant exercise meaningful vectors. AskMyDocs backend embedding and retrieval
integration remain later-epic work.

## Learning goals

By the end you should be able to explain and demonstrate:

- collection, shard, segment, point, vector, payload, and index boundaries;
- the write path through the write-ahead log (WAL) and segments;
- why a small collection may use exact scanning instead of HNSW;
- how HNSW parameters trade recall, index cost, memory, and latency;
- how the query planner combines vector similarity with payload filters;
- how updates, deletion, optimization, and persistence behave;
- which settings matter to a future local RAG system and which do not yet.

## Tutorial map

| Video-style tool | This repository |
|---|---|
| Mamba environment | isolated `uv` project |
| Jupyter as the only interface | small Python phases plus a companion notebook |
| `docker run` | pinned Docker Compose service |
| Faker payloads | frozen genuine Billboard chart facts |
| random NumPy vectors | local Nomic description embeddings |
| synthetic query vector | natural-language liking query embedded by the same model |

## Before Q00

Run from the repository root:

```bash
docker --version
docker compose version
uv --version
python3 --version
docker compose -f deployment/compose.qdrant.yaml config
uv sync --project sandbox/qdrant_music --extra dev --extra notebook
uv run --project sandbox/qdrant_music \
  python -m ipykernel install \
  --user \
  --name qdrant-music \
  --display-name "Python (Qdrant Music Tutorial)"
```

Expected: Docker and Compose print versions, Python 3.11 is available, Compose
configuration renders without error, and `uv` creates the sandbox environment.
The final command registers the exact kernel named in the companion notebook.

Common failure: if Docker commands cannot reach the daemon, start Docker
Desktop or the local Docker Engine before continuing.

---

## Q00 — Learning goals and prerequisites

### Goal

Know which process owns each responsibility.

### Internal mechanism

```text
Python/FastEmbed                      Qdrant
----------------                     -------------------------------
turns text into vectors       HTTP   validates collection schema
constructs point payloads   ------>  writes operations to the WAL
constructs query vectors             stores points in segments
renders returned results             plans and executes vector search
```

Qdrant does **not** understand a song, sentence, or lyric. It receives numbers,
IDs, and JSON payload. Semantic meaning exists because the same embedding model
maps related descriptions and queries into nearby locations.

### Try it yourself

Explain aloud which component would be wrong if a collection expects 384
dimensions but FastEmbed produces 768.

### Checkpoint

You can distinguish embedding inference from vector storage and search.

---

## Q01 — Qdrant's data model

### Goal

Understand where a point lives and which structures speed up access.

### Internal mechanism

```text
Qdrant process
└── collection
    └── shard
        ├── WAL
        └── segments
            ├── external ↔ internal ID mapping
            ├── vector storage
            ├── payload storage
            ├── plain or HNSW vector index
            └── optional payload indexes
```

- **Collection:** named set of points sharing vector schema and distance metric.
- **Shard:** unit of distribution and parallelism. This one-node lab uses one.
- **Segment:** independently searchable storage unit. Optimizers merge or
  rebuild segments in the background.
- **Point:** external integer/UUID ID, vector, and optional JSON payload.
- **Vector storage:** full-precision values used for scoring and recovery.
- **Vector index:** plain scan or HNSW navigation structure.
- **Payload index:** typed structure for efficient filtering and cardinality
  estimation.

### Similarity by hand

For vectors `a=(1, 1)` and `b=(2, 2)`, cosine similarity is:

```text
(a · b) / (||a|| × ||b||) = 4 / (√2 × √8) = 1
```

They point in the same direction even though their magnitudes differ. Nomic
embeddings use 768 dimensions, but Qdrant applies the same idea efficiently.

### Checkpoint

You can explain why payload fields are filterable facts while a vector is a
learned numeric representation.

---

## Q02 — Connect and inspect the server

### Goal

Start Qdrant, verify readiness, and connect with the official client.

### Run

```bash
docker compose -f deployment/compose.qdrant.yaml up -d
uv run --project sandbox/qdrant_music \
  python -m qdrant_music.tutorial_steps.q02_connect
```

Expected:

```text
Q02 — Connect and inspect the server
{
  "url": "http://localhost:6333/readyz",
  "status": "ready"
}
```

Inspect the service:

```bash
docker compose -f deployment/compose.qdrant.yaml ps
docker compose -f deployment/compose.qdrant.yaml logs --tail=50 qdrant
curl http://localhost:6333/telemetry
curl http://localhost:6333/metrics
```

### Internal mechanism

`/readyz` returns success after the node can serve requests. The Python client
sends HTTP requests to port 6333; port 6334 is the gRPC interface. Both are
bound to loopback by this lab, so the unsecured development server is not
published on the LAN.

### Common failure

Connection refused means the service is stopped or still starting. Run the
documented `wait-ready` command rather than adding arbitrary sleep calls.

### Checkpoint

The service is ready and `get_collections` succeeds.

---

## Q03 — Inspect and validate Billboard data

### Goal

Verify the input before storing anything.

### Run

```bash
uv run --project sandbox/qdrant_music \
  python -m qdrant_music.tutorial_steps.q03_validate_dataset
```

Expected summary:

```text
records: 50
rank_min: 1
rank_max: 50
duplicate_ids: 0
missing_descriptions: 0
valid: true
```

### Internal mechanism

Chart facts become payload. Original, manually reviewed descriptions and tags
provide text for the educational embedding. Stable UUIDv5 IDs derive from chart
date, rank, title, and artist, so rerunning an upsert replaces the same points.
The fixture checksum prevents an unnoticed data edit.

Read `sandbox/qdrant_music/fixtures/NOTICE.md` for provenance and restrictions.
No lyrics, audio, artwork, or copied reviews are included.

### Try it yourself

Open one record and decide which fields belong in a vector description and
which should remain exact payload filters.

### Checkpoint

Exactly 50 unique, reviewed records pass validation.

---

## Q04 — Generate and inspect an embedding

### Goal

Convert one description into the vector schema used by Qdrant.

### Run

```bash
uv run --project sandbox/qdrant_music \
  python -m qdrant_music.tutorial_steps.q04_embedding
```

First use may download `nomic-ai/nomic-embed-text-v1.5`. Expected:

```text
dimensions: 768
l2_norm: approximately 1
first_five_values: [...]
```

### Internal mechanism

Documents are prefixed with `search_document:` and queries with
`search_query:`. The prefix tells Nomic which retrieval role it is encoding.
The sandbox validates every vector length before sending it to Qdrant.

### Common failure

A missing network connection on first use prevents model download. Provision
the model once while online; subsequent use is local.

### Checkpoint

One description produces exactly 768 finite values.

---

## Q05 — Create the baseline collection

### Goal

Create an idempotent collection with explicit vector schema.

### Run

```bash
uv run --project sandbox/qdrant_music \
  python -m qdrant_music.tutorial_steps.q05_create_baseline
```

Important configuration:

```python
models.VectorParams(size=768, distance=models.Distance.COSINE)
```

### Internal mechanism

Collection creation establishes the invariant applied to every later upsert.
If the collection already exists, the code verifies size and distance. It never
silently deletes a mismatched collection.

The baseline keeps Qdrant defaults so you can observe its normal small-data
decision. It may show zero indexed vectors because an exact scan is cheaper.

### Checkpoint

Collection status is green and the vector schema is 768/cosine.

---

## Q06 — Trace and execute an upsert

### Goal

Store all 50 points and understand durability.

### Run

```bash
uv run --project sandbox/qdrant_music \
  python -m qdrant_music.tutorial_steps.q06_upsert
```

Expected:

```text
upserted: 50
exact_count: 50
```

### Internal mechanism

```text
client batch
  → schema validation
  → ordered WAL record
  → update worker
  → appendable segment
  → vector/payload storage
  → wait=True response after application
  → later background optimization
```

The WAL makes accepted operations replayable after abnormal shutdown. Each
operation has an order/version. Newer point versions win; duplicate physical
copies during optimization are deduplicated during search. `wait=True` waits
for application to storage, not for every later segment optimization.

### Try it yourself

Run the phase again. Count remains 50 because stable IDs make the operation
idempotent.

### Checkpoint

The exact count API returns 50 after two loads.

---

## Q07 — Inspect segments and collection state

### Goal

Distinguish approximate operational counters from exact logical count.

### Run

```bash
uv run --project sandbox/qdrant_music \
  python -m qdrant_music.tutorial_steps.q07_inspect
```

Inspect:

- collection status and optimizer status;
- exact count versus `points_count`;
- `indexed_vectors_count`;
- segment count;
- effective HNSW and optimizer configuration.

### Internal mechanism

During optimization, points can be copied between segments and old versions
can remain temporarily. Operational counters are useful signals but are not a
transactional record count. Use the exact count API when correctness requires
an exact number.

For only 50 × 768 float32 values (about 150 KiB before overhead), defaults may
leave the segment plain and report zero indexed vectors. That is an optimization,
not a failure.

### Checkpoint

You can explain why `exact_count=50` and `indexed_vectors_count=0` can both be
correct.

---

## Q08 — Run exact similarity search

### Goal

Establish ground truth using a full scan.

### Run

```bash
uv run --project sandbox/qdrant_music \
  python -m qdrant_music.tutorial_steps.q08_exact_search
```

Query:

```text
uplifting energetic pop with a strong dance feel
```

### Internal mechanism

With `exact=True`, Qdrant compares the query vector with every eligible vector,
sorts by cosine similarity, and returns top-k. This is deterministic ground
truth for comparing approximate methods, but its work grows linearly with the
candidate set.

Similarity is not probability. A score of 0.7 does not mean a 70% chance that
you like a song.

### Checkpoint

Five score-sorted results include payload explanations and no full vectors.

---

## Q09 — Build the HNSW learning collection

### Goal

Force an actual HNSW index for honest comparison.

### Run

```bash
uv run --project sandbox/qdrant_music \
  python -m qdrant_music.tutorial_steps.q09_build_hnsw
```

Tutorial overrides:

```python
m = 16
ef_construct = 100
full_scan_threshold = 10       # KiB
indexing_threshold = 10        # KiB
```

### Internal mechanism

HNSW stores vectors as graph nodes. Each node has nearby connections; upper
layers make long jumps and lower layers refine candidates. `m` controls graph
connectivity. `ef_construct` controls build-time exploration. The two low
thresholds exist only to make 50 records build and use HNSW.

The phase polls collection state until at least 50 indexed vectors are
reported. If it times out, do not claim that later searches use HNSW.

### Common failure

Changing HNSW configuration on existing data can trigger asynchronous segment
rebuilds. Wait for optimization rather than reading one immediate status.

### Checkpoint

The tuning collection reports 50 indexed vectors.

---

## Q10 — Compare exact and approximate search

### Goal

Measure the recall/latency control provided by query-time `hnsw_ef`.

### Run

```bash
uv run --project sandbox/qdrant_music \
  python -m qdrant_music.tutorial_steps.q10_compare_search
```

The phase compares exact top five with `hnsw_ef` 8, 32, and 128.

### Internal mechanism

Higher `hnsw_ef` keeps more candidates in the dynamic search list. It generally
improves recall but increases distance calculations and latency. Qdrant ensures
the effective candidate list is not smaller than `limit`.

With 50 points, HNSW can be slower than exact scan because graph traversal has
overhead. These timings teach controls; they are not capacity benchmarks.

### Checkpoint

You can calculate top-five overlap with exact results and explain any mismatch.

---

## Q11 — Run a personal liking query

### Goal

Change the query without changing stored vectors.

### Run

```bash
uv run --project sandbox/qdrant_music \
  python -m qdrant_music.tutorial_steps.q11_personal_query \
  --query "melancholic acoustic songs with calm intimate vocals"
```

Try:

- `happy celebratory high-energy music`
- `dark bass-heavy rap with tense energy`
- `warm romantic pop for a quiet evening`
- `country music for a lively road trip`

### Internal mechanism

Only the query is newly embedded. Qdrant searches the same stored vector space.
Returned descriptions and tags help you interpret why a match occurred.

### Checkpoint

Two materially different queries produce meaningfully different rankings.

---

## Q12 — Add filters and payload indexes

### Goal

Combine semantic ranking with exact constraints.

### Run

```bash
uv run --project sandbox/qdrant_music \
  python -m qdrant_music.tutorial_steps.q12_filters
```

The example requires tag `dance-pop` and chart rank at most 40, searches once,
creates typed indexes, then repeats.

### Internal mechanism

- `must`: every condition must match.
- `should`: at least one optional condition should match according to filter
  semantics.
- `must_not`: matching points are excluded.
- `match`: exact keyword/bool match.
- `range`: numeric or datetime bounds.
- `has_id`: constrain by point IDs.
- `nested`: apply conditions within the same nested object.

Payload indexes improve cardinality estimation and filtered traversal. They do
not change which documents logically match. Index fields you constrain often,
not every stored field.

### Checkpoint

Before/after results contain the same logical matches, all satisfying filters.

---

## Q13 — Explore parameter trade-offs

### Goal

Change one search parameter at a time and record the effect.

### Run

```bash
uv run --project sandbox/qdrant_music \
  python -m qdrant_music.tutorial_steps.q13_parameters
```

Experiment with CLI controls:

```bash
uv run --project sandbox/qdrant_music qdrant-music search \
  --kind hnsw \
  --query "upbeat dance music" \
  --hnsw-ef 32 \
  --score-threshold 0.30 \
  --limit 5 \
  --tag dance-pop \
  --max-chart-rank 40
```

### Checkpoint

For each change, state whether it primarily affects recall, latency, result
volume, memory, storage, or correctness.

---

## Q14 — Update, delete, and restore a point

### Goal

Observe logical mutation separately from later physical cleanup.

### Run

```bash
uv run --project sandbox/qdrant_music \
  python -m qdrant_music.tutorial_steps.q14_update_delete
```

Expected:

```text
count_after_delete: 49
count_after_idempotent_restore: 50
```

### Internal mechanism

Update and delete operations first enter the WAL. A delete updates logical
version state so search stops returning the point. Old bytes may remain until
the vacuum optimizer rebuilds a segment. Upsert with the same stable ID restores
the current point.

`deleted_threshold` and `vacuum_min_vector_number` prevent constant expensive
rebuilds for tiny numbers of deleted records.

### Checkpoint

One point can be updated, removed, and restored without recreating a collection.

---

## Q15 — Verify persistence

### Goal

Prove normal shutdown removes containers but preserves the named volume.

### Run

```bash
docker compose -f deployment/compose.qdrant.yaml down
docker compose -f deployment/compose.qdrant.yaml up -d
uv run --project sandbox/qdrant_music \
  python -m qdrant_music.tutorial_steps.q15_persistence
```

Expected: exact count remains 50.

### Internal mechanism

The named volume maps to `/qdrant/storage`. Normal Compose shutdown does not
delete it. On startup Qdrant loads persisted segments and can replay WAL work
that was accepted but not fully applied before an abnormal stop.

### Checkpoint

Both collection schema and all 50 logical points survive restart.

---

## Q16 — Final exercise and cleanup

### Goal

Complete the workflow without copying a prepared query.

### Run

```bash
uv run --project sandbox/qdrant_music \
  python -m qdrant_music.tutorial_steps.q16_final_exercise
```

Then:

1. Write a personal mood/style/context query.
2. Select exact or HNSW and justify it.
3. Add a tag or numeric filter.
4. Explain the top three using descriptions and tags.
5. Change `hnsw_ef` and report exact overlap.

Safe stop:

```bash
docker compose -f deployment/compose.qdrant.yaml down
```

> **Destructive reset — deletes all sandbox Qdrant data**
>
> ```bash
> docker compose -f deployment/compose.qdrant.yaml down --volumes
> ```

Collection-only cleanup is less destructive:

```bash
uv run --project sandbox/qdrant_music \
  qdrant-music collection delete --kind baseline
uv run --project sandbox/qdrant_music \
  qdrant-music collection delete --kind hnsw
```

---

# Parameter reference for Qdrant 1.18.2

Defaults below are documented/observed for the pinned version. A deployment can
override server defaults, so inspect `get_collection` rather than assuming.

## Vector and collection parameters

| Parameter | Scope | Tutorial value | Internal effect and trade-off | Rebuild/change guidance |
|---|---|---:|---|---|
| `size` | vector | 768 | Number of float components; determines compatibility and raw memory | Fixed for existing vector; use a new vector/collection for model dimension change |
| `distance` | vector | `Cosine` | Scoring function; must match embedding model behavior | Treat as schema; recreate/migrate deliberately |
| `datatype` | vector | float32 default | float16/uint8 can reduce memory with precision trade-off | Advanced; benchmark recall |
| `on_disk` | vector | `False` | RAM storage is fast; `True` uses memory mapping/page cache | Live update triggers background rebuild |
| named vectors | point | none | Multiple representations with independent schema | Useful for future multi-representation retrieval |
| `shard_number` | collection | 1 | Parallel/distributed partition count | Do not tune for this one-node lab |
| `replication_factor` | collection | 1 | Number of shard replicas | Requires cluster nodes to provide resilience |
| `write_consistency_factor` | collection | 1 | Replicas that must acknowledge writes | Higher can improve consistency but reduce availability |
| `on_disk_payload` | collection | `True` | Saves RAM for large payload; reads may incur I/O | Index filtered fields because indexes stay in RAM |
| `strict_mode_config` | collection | default | Limits expensive or unsafe queries/updates | Production guardrail; not disabled silently |
| `metadata` | collection | none | Stores collection-level model/migration facts, not point payload | Useful for schema provenance; does not affect search |

## HNSW and query-planning parameters

| Parameter | Default / tutorial | Effect | Cost | Rebuild? |
|---|---|---|---|---|
| `m` | 16 / 16 | Maximum graph connectivity per node | Higher recall and RAM/build time | Yes |
| `ef_construct` | 100 / 100 | Candidate exploration during graph build | Higher build quality and build time | Yes |
| `full_scan_threshold` | about 10000 KiB / 10 | Below estimate, planner prefers exact scan | Lower value forces graph use sooner | Yes/background segment rebuild |
| `max_indexing_threads` | 0 automatic | CPU threads per index build | More can speed builds but contend with queries | Applies to builds |
| HNSW `on_disk` | `False` | Memory-map graph | Lower required RAM, more page-cache/I/O sensitivity | Yes |
| `hnsw_ef` | defaults from collection / 8–128 | Query candidate breadth | Higher recall and latency | No |
| `exact` | `False` / comparison uses both | Bypass HNSW and scan eligible vectors | Exact recall, linear work | No |
| `indexed_only` | `False` | Avoid large unindexed segments | Stable latency but recent points may temporarily disappear | No |

`limit` effectively establishes a lower bound for search candidate capacity;
asking for more results cannot be served from fewer candidates.

## Optimizer parameters

| Parameter | Typical default | Meaning | When to change |
|---|---:|---|---|
| `indexing_threshold` | about 10000 KiB | Plain-vector data allowed before HNSW build | Lower only for learning/small indexed sets; use 0 to defer/disable indexing during controlled bulk load |
| `memmap_threshold` | unset/default policy | Segment size at which vectors become memory mapped | Large datasets with constrained RAM |
| `deleted_threshold` | 0.2 | Deleted fraction that can trigger vacuum | Tune only with measured delete/update workload |
| `vacuum_min_vector_number` | 1000 | Minimum segment size for vacuum | Prevents rebuilding tiny segments |
| `default_segment_number` | 0 automatic | Target segment parallelism | Balance query parallelism and optimizer overhead |
| `max_segment_size` | automatic | Prevent overly large segments | Large ingestion/index-build tuning |
| `flush_interval_sec` | 5 | Interval between forced storage flushes | Durability/I/O tuning; WAL still protects accepted operations |
| `max_optimization_threads` | automatic/version dependent | Concurrent optimizer jobs per shard | Limit write/query contention |
| `prevent_unoptimized` | `False` experimental | Defers visibility beyond threshold until indexed | Advanced latency control; coordinate with `wait=False` |

Optimizers perform indexing, merging, and vacuum work while searches continue.
Heavy writes can make optimizers compete with queries for CPU, memory, and I/O.

## WAL and write parameters

| Parameter | Meaning | Trade-off |
|---|---|---|
| `wal_capacity_mb` | Size target for WAL segments | Larger values reduce rotation frequency but retain more WAL data |
| `wal_segments_ahead` | Preallocated future WAL segments | Can smooth rotation at disk-space cost |
| `wait` | Wait until operation is applied and visible | Easier deterministic tutorials; higher request latency |
| `ordering` | weak, medium, or strong update ordering | Stronger coordination reduces write availability/throughput in clusters |
| upsert batch size | Points per request | Larger improves throughput until memory/request limits dominate |

The Python tutorial uses `wait=True` because each phase verifies state
immediately. High-throughput ingestion may choose a different acknowledgement
strategy.

## Query parameters

| Parameter | Meaning | Guidance |
|---|---|---|
| `query` | Dense vector or advanced query object | Must match vector name and dimension |
| `limit` | Maximum returned results | Keep only what the consumer needs |
| `offset` | Skip results | Exact stable pagination is expensive; cursor/ID strategies are often better |
| `score_threshold` | Minimum acceptable similarity | Model/metric specific; calibrate with evaluation data |
| `query_filter` | Exact payload constraints | Create indexes for selective, frequent fields |
| `with_payload` | Return metadata | Select fields for large payloads |
| `with_vectors` | Return stored vector | Usually false; vectors are large and rarely UI data |
| `search_params` | HNSW/exact/quantization controls | Tune per query class only after measuring |
| `timeout` | Server-side query limit | Bound expensive work and surface failure clearly |
| `consistency` | Replica read consistency | Meaningful in replicated clusters, not this lab |
| shard selector | Search selected shards/shard keys | Multitenant/distributed use only |

## Filter parameters and index types

- `must`, `should`, `must_not` combine conditions.
- keyword index supports exact string and array-element matches.
- integer/float indexes support ranges and equality.
- bool index supports boolean match.
- datetime index supports timestamp ranges.
- geo index supports radius, bounding-box, and polygon conditions.
- text index supports tokenized full-text/phrase behavior.
- UUID index supports UUID payload lookup.
- nested filters keep multiple conditions within one nested array object.

Indexing every field wastes memory and optimizer work. Index fields that often
reduce the candidate set.

## Quantization parameters

| Family/control | Purpose | Trade-off |
|---|---|---|
| scalar `int8` | Compress each component | Good general memory reduction with some approximation |
| product quantization | Encode subvector groups | Higher compression and training/build complexity |
| binary quantization | One/few bits per component | Very fast/compact for compatible high-dimensional models; recall depends on data |
| `always_ram` | Keep quantized representation in RAM | Faster traversal, more RAM |
| `quantile` | Exclude extreme scalar values from range estimation | Can improve useful precision but needs validation |
| `oversampling` | Retrieve extra approximate candidates | Better recall, more work |
| `rescore` | Score candidates with original vectors | Better final precision, additional reads/calculation |
| `ignore` | Bypass quantized scoring behavior | Diagnostic/quality control, potentially slower |

The lab does not enable quantization: 50 vectors do not justify it. The appendix
documents the controls for future measured experiments.

## Advanced capability map

| Capability | What Qdrant offers | AskMyDocs timing |
|---|---|---|
| sparse vectors | inverted-index lexical representations | later hybrid retrieval epic |
| hybrid/prefetch/fusion | combine dense, sparse, and multistage queries | later hybrid retrieval epic |
| recommendation | positive and negative example points/vectors | optional future experiment |
| discovery/context | navigate toward and away from contextual examples | optional future experiment |
| grouping | group results by payload field | later API need if justified |
| facets | counts for indexed keyword fields | possible inspection UI |
| multivectors | multiple token/late-interaction vectors per point | post-MVP research |
| multitenancy/shard keys | isolate/rout tenants in shared collections | future scale requirement |
| snapshots | consistent backup/recovery artifacts | operations stage |
| telemetry/metrics | service and collection operational visibility | later observability work |
| distributed replication | shard replicas and consistency controls | not needed for local MVP |

## Authoritative parameter decision matrix

The compact tables above explain concepts. The matrices below are the
authoritative checklist for the pinned server/client pair. `None → server`
means the Python client omits the field and Qdrant 1.18.2 applies its service
default. Thresholds are KiB of vector data, not point counts. “Rebuild” means a
background segment/index rebuild may be scheduled; it does not mean the
collection must be deleted.

### Vector and collection schema

| Exact Python name / REST field | Scope | 1.18.2 default | Tutorial | Internal component | Trade-off and rebuild | Later AskMyDocs use / do not change when |
|---|---|---|---|---|---|---|
| `models.VectorParams(size=...)` / `vectors.size` | named or unnamed dense vector | required | `768` | vector schema and scorer | Linear RAM/disk/compute growth; schema migration, not an in-place rebuild | Match the selected embedding model; never guess or truncate dimensions |
| `models.VectorParams(distance=...)` / `vectors.distance` | vector | required | `Cosine` | score function; cosine normalizes at upload | Changes ranking semantics; migrate/recreate deliberately | Match model training; do not tune as a latency control |
| `models.VectorParams(datatype=...)` / `vectors.datatype` | vector | `float32` | omitted/`float32` | stored vector representation | `float16`/`uint8` save space with precision constraints; rebuilding/migration required | Consider only with model-compatible evaluation; do not cast Nomic output casually |
| `models.VectorParams(on_disk=...)` / `vectors.on_disk` | vector | `None` service policy, effectively RAM for this image | omitted | vector storage/memmap | Saves RAM, adds page-cache I/O; update rebuilds affected segments | Consider beyond RAM budget; keep RAM for this 50-point lab |
| `vectors_config={"name": VectorParams(...)}` / named vectors map | collection/point | none | one unnamed vector | vector registry and per-vector indexes | Each vector adds storage/index cost; adding one builds its index | Use for distinct dense/sparse representations; do not create names without a retrieval need |
| `shard_number` / `shard_number` | collection | one shard on this single node | omitted | shard routing/parallelism | More shards add segment/WAL overhead; resharding is operational work | Revisit only for measured scale/distribution; not for 50 points |
| `replication_factor` / `replication_factor` | collection | `1` | omitted | replica placement | More disk/network/write work for resilience; cluster operation | Use only with multiple nodes and an availability target |
| `write_consistency_factor` / `write_consistency_factor` | collection | `1` | omitted | replica acknowledgement | More acknowledgements can reduce write availability; no index rebuild | Choose with replication semantics; meaningless on this one-node lab |
| `on_disk_payload` / `on_disk_payload` | collection | `True` | omitted (`True`) | payload storage | Lower RAM, possible payload-read I/O; payload indexes remain RAM-resident; no vector rebuild | Retain for large document metadata; do not force RAM without measurement |
| `metadata` / `metadata` | collection | none | omitted | collection configuration/consensus | Negligible search cost; no index rebuild | Record embedding/schema version later; do not put per-point facts here |
| `strict_mode_config` / `strict_mode_config` | collection | disabled/unset in OSS image | omitted | request admission and guardrails | Can reject expensive limits, exact search, or unindexed filters; no rebuild | Enable measured production limits later; do not enable mid-tutorial and mistake rejection for a search bug |

### HNSW and optimizer controls

| Exact Python name / REST field | Scope | 1.18.2 default | Tutorial | Internal component | Trade-off and rebuild | Later AskMyDocs use / do not change when |
|---|---|---|---|---|---|---|
| `models.HnswConfigDiff(m=...)` / `hnsw_config.m` | collection/vector | `16` | `16` | graph degree | Higher recall, RAM, disk, and build time; **rebuilds HNSW** | Tune after recall tests; not to fix embedding quality |
| `ef_construct` / `hnsw_config.ef_construct` | collection/vector | `100` | `100` | graph construction search | Higher graph quality and build CPU/time; **rebuilds HNSW** | Tune for large stable corpora; not per query |
| `full_scan_threshold` / `hnsw_config.full_scan_threshold` | collection/vector | `10000` KiB | baseline `10000`, HNSW lab `10` | query planner/index policy | Lower forces graph use sooner and may waste work on tiny sets; **rebuild can occur** | Let defaults handle small filtered sets; lower here only to expose HNSW |
| `max_indexing_threads` / `hnsw_config.max_indexing_threads` | collection/vector | `0` auto | omitted | index builder thread pool | Faster builds can contend with queries; applies to subsequent rebuilds | Bound during production bulk indexing; not a search-thread control |
| `on_disk` / `hnsw_config.on_disk` | collection/vector | `False` | omitted | HNSW graph storage | Saves RAM with page-cache/I/O cost; **rebuilds HNSW** | Consider when graph exceeds RAM; avoid for this lab |
| `models.SearchParams(hnsw_ef=...)` / `params.hnsw_ef` | query | collection/server choice | `8`, `32`, `64`, `128` | graph traversal candidate queue | Higher recall/latency, no rebuild | Tune by query class and evaluation; do not assume bigger is always faster |
| `models.SearchParams(exact=...)` / `params.exact` | query | `False` | both | query planner/scorer | Full scan gives exact recall with linear work, no rebuild | Evaluation/diagnostics; avoid for large routine searches |
| `models.SearchParams(indexed_only=...)` / `params.indexed_only` | query | `False` | omitted | segment selection | Stable indexed-only latency can omit recent unindexed data, no rebuild | Rare latency SLO tool; do not use when freshness matters |
| `models.OptimizersConfigDiff(indexing_threshold=...)` / `optimizers_config.indexing_threshold` | collection | `10000` KiB | baseline `10000`, HNSW lab `10` | indexing optimizer | Lower builds HNSW earlier; background segment rebuild | Bulk-load with `0`, then restore; do not benchmark 50-point timings |
| `memmap_threshold` / `optimizers_config.memmap_threshold` | collection | unset/disabled | omitted | indexing optimizer/vector storage | Moves large segments to memmap, reducing RAM with I/O; rebuild | Use after capacity sizing; do not combine changes without attribution |
| `deleted_threshold` / `optimizers_config.deleted_threshold` | collection | `0.2` | omitted | vacuum optimizer | Lower reclaims sooner but rewrites more often; vacuum rebuild | Tune for measured churn; not after a single tutorial delete |
| `vacuum_min_vector_number` / `optimizers_config.vacuum_min_vector_number` | collection | `1000` | omitted | vacuum optimizer | Prevents expensive rewrites of tiny segments; vacuum rebuild | Lower only for unusual small/high-churn production sets |
| `default_segment_number` / `optimizers_config.default_segment_number` | shard | `0` auto | omitted | merge optimizer/search parallelism | More segments add parallelism and overhead; merges/rebuilds | Align with CPU/search load; never equate one segment with one shard |
| `max_segment_size` / `optimizers_config.max_segment_size` | shard | `None` auto | omitted | merge optimizer | Smaller caps build duration but increases segment fan-out; merges/rebuilds | Consider for very large indexes; avoid premature tuning |
| `flush_interval_sec` / `optimizers_config.flush_interval_sec` | shard | `5` seconds | omitted | segment flusher | Lower increases disk I/O; WAL still protects accepted writes; no HNSW rebuild by itself | Tune only with durability/I/O evidence |
| `max_optimization_threads` / `optimizers_config.max_optimization_threads` | shard | `None` dynamic | omitted | optimizer scheduler | More throughput, more CPU/I/O contention; affects future jobs | Bound during ingestion windows; `0` disables optimization and is risky |
| `prevent_unoptimized` / `optimizers_config.prevent_unoptimized` | collection | `False` | omitted | update admission/optimizer | Experimental backpressure protects reads but can delay visibility; no direct rebuild | Consider only with a documented backlog policy; not for normal MVP writes |

### WAL, writes, and query request controls

| Exact Python name / REST field | Scope | 1.18.2 default | Tutorial | Internal component | Trade-off and rebuild | Later AskMyDocs use / do not change when |
|---|---|---|---|---|---|---|
| `models.WalConfigDiff(wal_capacity_mb=...)` / `wal_config.wal_capacity_mb` | shard | `32` MiB | omitted | WAL segment rotation | Larger segments reduce rotation and retain more disk; no index rebuild | Tune from write volume/recovery tests; not search performance |
| `wal_segments_ahead` / `wal_config.wal_segments_ahead` | shard | `0` | omitted | WAL preallocation | Smoother rotation for bursty writes at disk cost; no rebuild | Consider sustained ingestion only |
| `wait` / write query parameter | operation | `False` client/API default | `True` | update acknowledgement/apply worker | Deterministic visibility versus response latency; no rebuild | Use for synchronous admin flows; batch ingestion may acknowledge earlier |
| `ordering` / write query parameter | operation | `weak` | omitted/weak | distributed update routing | `medium`/`strong` coordinate more and reduce availability/throughput; no rebuild | Choose only with replicated ordering requirements |
| `points=[...]` batch length / upsert body | request | caller chosen; service request cap 32 MiB | one batch of `50` | HTTP parser, WAL/update worker | Larger batches amortize overhead but use request/worker memory; no rebuild itself | Size by measured throughput and retry cost; never exceed service limits |
| `limit` / `limit` | query | endpoint-specific (`10` for universal query APIs) | `5` | candidate heap/result serialization | More candidates, scoring, network, and payload work; no rebuild | Return only useful chunks; not a recall substitute |
| `offset` / `offset` | query | `0` | omitted | result heap/pagination | Deep offsets still require finding skipped neighbors; no rebuild | Small UI paging only; avoid deep vector pagination |
| `score_threshold` / `score_threshold` | query | none | adjustable | final score filter | Fewer low-score results; wrong threshold harms recall; no rebuild | Calibrate per model/metric using evals, not intuition |
| `query_filter` / `filter` | query | none | tag/rank/weeks | filter planner, payload indexes, vector traversal | Selectivity can accelerate search; unindexed scans cost CPU; no vector rebuild | Enforce document/tenant facts; never encode permissions only in prompt text |
| `with_payload` / `with_payload` | query | `True` in client call here | `True` | payload retrieval/serialization | More disk/network for large payloads; no rebuild | Select required fields later; avoid shipping full chunks unnecessarily |
| `with_vectors` / `with_vector` | query | `False` | adjustable, default `False` | vector retrieval/serialization | Large response and disk/RAM copy cost; no rebuild | Diagnostics/export only; not normal RAG responses |
| `timeout` / `timeout` | request/query | client `30s`; server optional | client `30s` | request deadline | Bounds tail work but can expose partial failure; no rebuild | Set from API SLOs; do not use to hide poor plans |
| `consistency` / `consistency` | read | server default | omitted | replica read selection | Stronger reads coordinate replicas and may add latency/unavailability; no rebuild | Distributed correctness policy only |
| `shard_key_selector` / `shard_key` | read/write | all relevant shards | omitted | custom shard routing | Reduces fan-out and isolates tenants, but wrong key misses data; no rebuild | Future multitenancy after design; not on one automatic shard |

### Filters and payload indexes

`models.Filter(must=..., should=..., must_not=...)` maps to the same REST
fields. `must` is AND, `should` requires one listed condition when present, and
`must_not` excludes matches. These clauses alter planning, not vector storage,
and never rebuild HNSW by themselves.

| Python/API condition or index type | Tutorial | Internal behavior and cost | Later AskMyDocs use / avoid |
|---|---|---|---|
| `FieldCondition(match=MatchValue(...))` / keyword index | `community_tags` | Exact scalar/array-element lookup; index creation builds a payload index and consumes RAM | tenant IDs, sources, tags; not stemming/full text |
| `FieldCondition(range=Range(...))` / integer index | rank and weeks | `gt/gte/lt/lte` range pruning and cardinality estimate; index build uses RAM/disk | dates, sizes, page numbers where numeric meaning is real |
| `MatchAny(any=[...])` and `MatchExcept(except=[...])` / keyword index | documented, not run | Set inclusion/exclusion; large lists cost request and matching work | ACL/tag sets; avoid enormous ad-hoc lists |
| `IsEmptyCondition`, `IsNullCondition` | documented, not run | Tests missing/empty/null payload states | data-quality queries; avoid ambiguous schemas |
| `HasIdCondition(has_id=[...])` | documented, not run | Restricts to external point IDs using ID tracker | known-candidate rescoring; not semantic discovery |
| `NestedCondition(nested=...)` / nested indexes | documented, not run | Keeps conditions bound to the same array object | structured authors/sections; unnecessary for flat payloads |
| `PayloadSchemaType.KEYWORD` | tags | hash/map-style exact filtering and facets | categorical fields; not prose |
| `INTEGER`, `FLOAT`, `DATETIME` | rank, weeks, date | typed equality/range structures; index creation is a payload-index build, not HNSW | frequent selective ranges; avoid indexing unused fields |
| `BOOL`, `GEO`, `TEXT`, `UUID` | appendix only | specialized boolean, spatial, tokenizer, or UUID indexes | add only when payload semantics and query workload require them |

Payload indexes change filter execution cost and planner estimates, not filter
meaning. Creating or changing one builds that payload index; it does **not**
re-embed points or rebuild the dense HNSW graph.

### Quantization search controls

| Exact Python name / REST field | 1.18.2 default | Tutorial | Internal component | Trade-off and rebuild | Later AskMyDocs use / do not change when |
|---|---|---|---|---|---|
| `models.ScalarQuantization(...)` / `quantization_config.scalar` | disabled | disabled | compressed vector store | Usually int8: lower RAM/faster distance with recall loss; enabling **builds quantized data** | Evaluate on a representative corpus; not for 50 vectors |
| `models.ProductQuantization(...)` / `quantization_config.product` | disabled | disabled | subvector codebooks | High compression, training/build cost and approximation; **rebuilds quantized data** | Very large corpora only after scalar baseline |
| `models.BinaryQuantization(...)` / `quantization_config.binary` | disabled | disabled | bit-packed vector store | Extreme compression/fast bit scoring, model-dependent recall; **rebuilds quantized data** | Compatible high-dimensional models only |
| `always_ram` / quantizer `always_ram` | implementation/config dependent | omitted | quantized-vector residency | Faster access versus RAM use; may reload/rebuild representation | Keep compressed codes hot only when measured |
| `models.QuantizationSearchParams(oversampling=...)` / `params.quantization.oversampling` | none | omitted | approximate candidate stage | More candidates improve recall and cost latency; no rebuild | Tune with recall/latency curves |
| `ignore` / `params.quantization.ignore` | `False` | omitted | query planner | Bypasses quantized search for diagnosis/quality at higher cost; no rebuild | Compare quality; not a permanent unexplained override |
| `rescore` / `params.quantization.rescore` | server/config choice | omitted | full-vector final scorer | Better precision with extra vector reads/CPU; no rebuild | Retain when original-vector rescoring meets latency goals |

### Advanced and distributed controls not simulated here

| Capability and primary API/config | Default/tutorial | Internal component and trade-off | Later AskMyDocs use / when not |
|---|---|---|---|
| sparse vectors: `sparse_vectors_config`, `SparseVectorParams` | none/not run | inverted index adds lexical storage/build/update work | hybrid retrieval epic; not fake sparse values |
| hybrid: `query_points(prefetch=..., query=FusionQuery(...))` | none/not run | runs staged dense/sparse retrieval and fusion | after separate retrievers are evaluated |
| recommendation: `RecommendQuery` | not run | derives query from positive/negative examples | optional personalization, not base document QA |
| discovery/context: `DiscoverQuery`, context pairs | not run | scores target similarity plus contextual direction | research feature only with a clear UX |
| grouping: `query_points_groups(group_by=...)` | not run | over-fetches then groups payload values | deduplicate by document/source if product needs it |
| facets: `facet(key=...)` | not run | counts values through a payload index | inspection UI; do not facet unindexed high-cardinality prose |
| multivectors: `MultiVectorConfig` | none/not run | stores multiple vectors per point and aggregate scoring | late-interaction research; substantial storage cost |
| multitenancy: custom sharding and tenant payload index | automatic shard/not run | routes tenant data and reduces filter fan-out | only after tenant model/authorization design |
| snapshots: collection/full snapshot APIs | manual/not run | consistent storage archive with disk/I/O cost | operations/backup stage; not a substitute for tested restore |
| telemetry: `/telemetry`, `/metrics` | enabled/inspected | process/collection observability; small runtime cost | local and later observability; never send secrets in labels |
| distributed: `replication_factor`, consistency, shard transfer | cluster disabled/not run | consensus, network replicas, failure recovery | only when one-node local-first limits are intentionally exceeded |

## Authoritative references

- [Qdrant overview](https://qdrant.tech/documentation/overview/)
- [Collections](https://qdrant.tech/documentation/manage-data/collections/)
- [Storage and WAL](https://qdrant.tech/documentation/manage-data/storage/)
- [Indexing](https://qdrant.tech/documentation/manage-data/indexing/)
- [Optimizer](https://qdrant.tech/documentation/operations/optimizer/)
- [Filtering](https://qdrant.tech/documentation/search/filtering/)
- [Performance optimization](https://qdrant.tech/documentation/operations/optimize/)
- [Monitoring](https://qdrant.tech/documentation/operations/monitoring/)
- [FastEmbed supported models](https://qdrant.github.io/fastembed/examples/Supported_Models/)
