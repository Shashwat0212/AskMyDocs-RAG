# Epic 5 — Profiles And Navigator

Tickets: `RAG-029`–`RAG-037`

Runtime: Free-tier Colab

Status: Planned

## Goal

Use the Epic 4 benchmark to identify useful configuration profiles and train two small, explainable decision trees: one for ingestion/index settings and one for query-time retrieval settings.

## Profile Meaning

A profile is an immutable, named, versioned configuration.

An ingestion/index profile controls settings that require building or rebuilding a collection:

- Parser and chunking strategy.
- Chunk size and overlap.
- Dense and sparse models.
- Vector dimensions and normalization.
- Qdrant distance, HNSW, optimizer, quantization, and payload-index settings.
- Resource requirements and a compatibility hash.

A query profile controls settings that may change without rebuilding the collection:

- Dense and sparse candidate limits.
- Fusion method and parameters.
- Filters and score thresholds.
- Reranker enablement and candidate bounds.
- Final result count.
- Required collection capabilities.

Every retrieval trace and answer records both profile IDs and versions.

## Bounded Experiment Strategy

Do not run every possible combination.

1. Start from dense-only, sparse-only, hybrid, and hybrid-plus-reranker baselines.
2. Change one configuration family at a time on development data.
3. Remove clearly dominated configurations.
4. Combine only promising settings.
5. Run the 100-million-token tier only for baselines and shortlisted candidates.
6. Open the locked holdout only for final profile promotion.

Epic 5 records embedding time, index-build time, query P50/P95, RAM, disk, failures, and exact configuration alongside retrieval quality.

## Choosing A Winning Profile

For each benchmark situation:

1. Keep configurations within two absolute percentage points of the best evidence Recall@5.
2. Among those, maximize nDCG@5.
3. If quality remains within one point, prefer lower P95 latency.
4. Then prefer lower RAM and storage use.

The result becomes the training label for the navigator. A winning run never silently changes a product default; profile promotion requires review and a recorded decision.

## Corpus Scanner And Ingestion Navigator

Before indexing, scan the corpus for:

- Total extracted tokens and document count.
- Median, P95, and variance of document lengths.
- Language and extraction quality.
- Heading, section, table, list, and paragraph density.
- Numeric, entity, and domain-term density.
- Duplicate and near-duplicate ratios.
- Available runtime resources.

Do not give the decision tree labels such as “finance” or “technical.” It must choose from measurable features.

Train the ingestion tree from the 45 corpus observations and their experiment-derived profile labels. Use maximum depth 3, at least four observations per leaf, and grouped validation so variants from the same corpus family do not leak between training and validation.

## Query Scanner And Query Navigator

For each query, scan:

- Query length.
- Lexical rarity relative to the corpus.
- Names, dates, numbers, and quoted phrases.
- Question type and domain-term density.
- Estimated lexical versus semantic dependence.
- Estimated single-evidence versus multi-evidence need.
- Collection capabilities and ingestion-profile compatibility.

Train the query tree from per-query experiment results. Use maximum depth 5, at least ten queries per leaf, and grouped validation by source document and corpus family.

The query navigator may only select settings compatible with the existing collection. It cannot change parser, chunking, embedding, dimensions, distance, or index settings.

## Navigator Interfaces

```text
scan_corpus(corpus_manifest, resource_budget) -> CorpusScanResult
select_ingestion_profile(corpus_scan) -> ProfileSelection

scan_query(query, corpus_statistics, collection_capabilities) -> QueryScanResult
select_query_profile(query_scan) -> ProfileSelection
```

`ProfileSelection` returns:

- Selected profile ID and version.
- Confidence.
- Decision-tree version.
- Feature snapshot.
- Human-readable decision path.
- Compatibility result.
- Fallback state and reason.

## Safe Fallback

Use the reviewed `safe-default` profile when:

- Confidence is below `0.70`.
- Required scan features are missing.
- A feature falls outside the validated range.
- The selected query profile is incompatible with the collection.

The trace must record `fallback=true` and the reason. Epic 5 selects and approves the versioned `safe-default` from holdout evidence.

## Tickets

- `RAG-029`: ingestion/query profile schemas and winner-label rules.
- `RAG-030`: deterministic corpus and query feature extractors.
- `RAG-031`: bounded, checkpointed, resumable experiment runner.
- `RAG-032`: development-set configuration screening.
- `RAG-033`: Pareto analysis and candidate-profile creation.
- `RAG-034`: ingestion-profile decision tree.
- `RAG-035`: query-profile decision tree.
- `RAG-036`: navigator integration, confidence, compatibility, fallback, and trace provenance.
- `RAG-037`: locked-holdout validation and promotion of final profiles plus `safe-default`.

## Completion Criteria

- Experiment manifests reproduce every profile comparison.
- Development and holdout data remain separated.
- Profile schemas prevent incompatible query-time choices.
- Both decision trees are deterministic, explainable, and validated with grouped splits.
- Missing, out-of-range, low-confidence, and incompatible inputs use the safe fallback.
- Final profiles report quality, latency, memory, storage, corpus size, and validation evidence.
- Selected profiles can be handed to Epic 6 and rebuilt locally in Epic 7.
