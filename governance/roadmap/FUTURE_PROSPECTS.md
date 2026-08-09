# Future Prospects

## Purpose

This register captures possible future project directions explored during planning. A prospect is not an approved commitment until its status is `Approved`, the roadmap and decision log are updated, and an implementation handoff is prepared when needed.

## Statuses

- `Exploring`: early investigation with material unknowns.
- `Proposed`: sufficiently defined for project-owner review.
- `Approved`: accepted and promoted into the roadmap or an architecture plan.
- `Deferred`: valid direction intentionally postponed.
- `Rejected`: considered and intentionally not pursued.

## Current Prospects

Approved retrieval experimentation prospects have been promoted into Phase 1 Epics 4 and 5. Session memory is deferred outside Phase 1, and TurboQuant remains exploratory.

ID: PROSPECT-001
Title: Evaluate TurboQuant For Compressed Document-Vector Storage And Indexing
Status: Exploring
Target Stage Or Epic: Future research after Epic 5 establishes the compatible Qdrant experiment boundary
Last Reviewed: 2026-08-04
Rationale: Google presents TurboQuant as an online vector-quantization method for reducing memory overhead in vector search. The project should determine whether it can reduce local storage and memory use for document embeddings without unacceptable retrieval or answer-quality loss.
Proposed Direction: Prototype compression of document embeddings before or during Qdrant indexing, evaluating multiple bit widths and whether compressed vectors can be queried directly or require dequantization or a custom adapter. Treat source documents and dataset manifests as canonical and compressed Qdrant collections as rebuildable experimental indexes. Compare against the uncompressed Qdrant baseline.
Dependencies: A stable document ingestion and embedding/indexing pipeline; representative registered datasets; a free and reproducible TurboQuant prototype; Qdrant compatibility testing; retrieval and end-to-end answer-quality evaluation tooling.
Risks: TurboQuant may not be a drop-in Qdrant storage or query strategy and may require an adapter or custom vector-index path. Quantization distortion could reduce recall, citation correctness, or answer quality. Compression, dequantization, filtering, persistence, and recovery behavior may add latency or operational complexity.
Evidence: [Google Research: TurboQuant](https://research.google/blog/turboquant-redefining-ai-efficiency-with-extreme-compression/); [TurboQuant paper](https://arxiv.org/abs/2504.19874). The paper reports nearest-neighbor search experiments, but project-specific compatibility and quality impact remain unverified.
Resulting Decision: No architecture or roadmap decision yet; experiment required. Promotion, deferral, or rejection should follow a reproducible benchmark covering memory and disk reduction, index build and rebuild time, query latency, Recall@k or nDCG, result overlap, end-to-end answer quality, citation correctness, and Qdrant filtering, persistence, and recovery.

ID: PROSPECT-002
Title: Build An Isolated Qdrant Configuration Experiment Lab
Status: Approved
Target Stage Or Epic: Phase 1 Epics 4–5, `RAG-022`–`RAG-037`
Last Reviewed: 2026-08-09
Rationale: Qdrant collection and query choices should be tested against representative datasets instead of selected from generic defaults. A small database-and-client laboratory can isolate those choices without requiring document ingestion, generation, prompting, citations, a UI, or any other end-to-end RAG component.
Proposed Direction: Prototype a configuration-driven path from dataset and vector preparation through collection creation, point insertion, simple queries, and measured comparison. Experiment profiles may vary vector dimension and distance, HNSW and optimizer settings, payload indexes and metadata filters, exact versus approximate search, top-k, score thresholds, and returned fields. Record the dataset and query IDs, vector source, full configuration, collection state, retrieval metrics, latency, resource observations, and results for every run.
Dependencies: The pinned self-managed Qdrant server/client in Colab; deterministic datasets and queries; vector or embedding preparation; relevance judgments where quality metrics require them; and versioned run-manifest/result formats.
Risks: Small or unrepresentative datasets may produce misleading recommendations. Changing multiple parameters together can hide causality, while unrestricted permutations can make runs expensive and difficult to interpret.
Evidence: Initial implementation and experiment design should use the [Qdrant indexing documentation](https://qdrant.tech/documentation/manage-data/indexing/), [Qdrant search documentation](https://qdrant.tech/documentation/search/search/), and project-specific measurements rather than vendor defaults alone.
Resulting Decision: Promoted into the Epic 4 benchmark and Epic 5 experiment runner. Runs must use versioned profiles/manifests, the approved development/holdout split, unique collections, checkpointed Drive artifacts, and reviewed profile promotion. See the 2026-08-09 benchmark and navigator decisions in `governance/decisions/DECISIONS.md`.

ID: PROSPECT-003
Title: Experiment With Vector Dimensions And Distance Metrics By Use Case
Status: Approved
Target Stage Or Epic: Phase 1 Epic 5 experiment family
Last Reviewed: 2026-08-04
Rationale: There is no universally best vector dimension or distance metric. Suitable choices depend on the embedding model, normalization behavior, dataset, retrieval task, quality target, storage budget, and local hardware.
Proposed Direction: Use the isolated Qdrant lab to compare model-native dimensions and officially supported dimension reduction, never arbitrary truncation without documenting its validity risk. Compare cosine, dot product, Euclidean, and Manhattan distance with normalized and non-normalized vectors where meaningful. Measure Recall@k, nDCG or MRR when labels permit, result overlap, latency, RAM, disk, and index-build cost.
Dependencies: PROSPECT-002; embedding models or vector sources with documented dimensions and normalization behavior; representative datasets; fixed query and relevance sets; and repeatable collection profiles.
Risks: Comparing different dimensions across different models can confound model quality with dimension effects. An incompatible metric or unsupported truncation can invalidate the vector space and make apparently fast results meaningless.
Evidence: Qdrant states that vector size comes from the selected model and documents the supported metrics in its [semantic search guide](https://qdrant.tech/documentation/tutorials-basics/search-beginners/) and [search documentation](https://qdrant.tech/documentation/search/search/). Supported dimension reduction should be grounded in model documentation or methods such as [Matryoshka Representation Learning](https://arxiv.org/abs/2205.13147).
Resulting Decision: Promoted as an Epic 5 experiment family. Produce per-dataset/model guidance and Pareto trade-offs, not a global dimension or metric. Selected defaults require versioned benchmark evidence and profile review.

ID: PROSPECT-004
Title: Tune HNSW And Research Alternative Approximate Nearest-Neighbor Methods
Status: Approved
Target Stage Or Epic: Phase 1 Epic 5 experiment family
Last Reviewed: 2026-08-04
Rationale: HNSW search quality and cost depend on dataset scale, update behavior, filters, hardware, and graph settings. Alternative approximate nearest-neighbor methods may offer different memory, build-time, update, persistence, or latency trade-offs.
Proposed Direction: Run controlled Qdrant profiles varying `m`, `ef_construct`, `hnsw_ef`, `full_scan_threshold`, indexing thresholds, index placement, and exact versus approximate search. Measure Recall@k or nDCG, P50/P95 latency, index-build time, RAM, disk, update cost, and interactions with selective payload filters. Separately research DiskANN, IVF-based indexes, ScaNN, graph variants, and compression-aware search, cross-referencing PROSPECT-001 for TurboQuant.
Dependencies: PROSPECT-002; datasets large enough to exercise approximate indexing honestly; exact-search ground truth; repeatable load and query workloads; and resource measurement tooling.
Risks: Tiny collections can make full scan faster and conceal HNSW behavior. Results from one ANN implementation may not transfer to Qdrant, and alternative methods may conflict with local-first persistence, filtering, update, or operational requirements.
Evidence: Start with Qdrant's [indexing documentation](https://qdrant.tech/documentation/manage-data/indexing/) and compare primary research such as [DiskANN](https://www.microsoft.com/en-us/research/publication/diskann-fast-accurate-billion-point-nearest-neighbor-search-on-a-single-node/) and [ScaNN](https://arxiv.org/abs/1908.10396). Project-specific compatibility and quality remain unverified.
Resulting Decision: HNSW, exact-search, optimizer, payload-filter, and resource comparisons are promoted into Epic 5. Alternative ANN engines remain research-only unless separately approved because Qdrant is the Phase 1 retrieval engine.

ID: PROSPECT-005
Title: Compare Local Embedding Models In An Isolated Embedding Lab
Status: Approved
Target Stage Or Epic: Phase 1 Epic 5 experiment family
Last Reviewed: 2026-08-04
Rationale: The planned Nomic and BGE models are starting points, not universal winners. The project needs a clear view of which free local models fit particular languages, domains, retrieval tasks, context lengths, and hardware limits.
Proposed Direction: Create an independently runnable Colab embedding laboratory that embeds common datasets, records model metadata and instructions, and exports compatible vectors and manifests to the Qdrant lab. Compare retrieval quality, native and supported reduced dimensions, context length, language coverage, query/document instruction format, CPU and RAM use, latency, model size, licensing, and quantization support.
Dependencies: Shared datasets and query judgments; reproducible self-managed model execution; model cards and licenses; common timing and resource measurements; and the Qdrant lab for downstream retrieval comparison.
Risks: Public leaderboard rank may not predict project-domain quality. Incorrect query prefixes, pooling, normalization, truncation, or licensing assumptions can invalidate comparisons or prevent later use.
Evidence: Use the [MTEB paper](https://arxiv.org/abs/2210.07316) and [MTEB documentation](https://docs.mteb.org/overview/) as benchmark references, then validate against project datasets. Initial planned-model evidence includes the [Nomic Embed v1.5 model card](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5) and [BGE Small EN v1.5 model card](https://huggingface.co/BAAI/bge-small-en-v1.5).
Resulting Decision: Promoted through the Epic 4 dataset registry and the Epic 5 profile schema and experiment runner. Produce use-case guidance rather than one universal model ranking; selected defaults must be captured in reviewed profiles and summary reports.

## Component Laboratory Convention

Approved component experiments run through the Epic 5 Colab experiment runner, not as permanent duplicate applications or automatic production tuners. They use the Epic 4 benchmark, configuration-driven profiles, deterministic corpus/query identifiers, unique collection/output names, explicit baselines, exact run manifests, checkpointed/resumable execution, and repeatable evaluation. Qdrant runs ephemerally on the Colab filesystem. Shared Drive holds datasets and full artifacts; Git receives reviewed code, compact fixtures, selected profiles, manifests, and summaries. Paid services, hosted inference, hosted vector databases, unbounded matrices, and unattended scheduling remain prohibited. A winning run does not silently change product defaults.

## Entry Template

Copy this section for each new prospect and replace `PROSPECT-NNN` with the next sequential identifier.

```text
ID: PROSPECT-NNN
Title:
Status: Exploring | Proposed | Approved | Deferred | Rejected
Target Stage Or Epic:
Last Reviewed: YYYY-MM-DD
Rationale:
Proposed Direction:
Dependencies:
Risks:
Evidence:
Resulting Decision:
```

## Promotion Rule

When a prospect becomes `Approved`:

1. Update its status and last-reviewed date.
2. Update `governance/roadmap/ROADMAP.md` or the relevant file under `governance/phase-1/`.
3. Add an active entry to `governance/decisions/DECISIONS.md` when the approval changes architecture, tooling, models, workflow, or repository conventions.
4. Link the resulting decision from the prospect.
5. Prepare a focused handoff under `governance/handoffs/` before implementation starts.

Rejected and deferred prospects remain in this file so the reasoning is not lost.
