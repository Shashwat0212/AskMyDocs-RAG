# Future Prospects

## Purpose

This register captures possible future project directions explored during planning. A prospect is not an approved commitment until its status is `Approved` and the resulting roadmap, architecture, and decision changes are merged into `main`.

## Statuses

- `Exploring`: early investigation with material unknowns.
- `Proposed`: sufficiently defined for project-owner review.
- `Approved`: accepted and promoted into the roadmap or an architecture plan.
- `Deferred`: valid direction intentionally postponed.
- `Rejected`: considered and intentionally not pursued.

## Current Prospects

Phase 1 Epics 7 through 9 are already approved planning items and remain in `docs/architecture/phase_1_core_rag_mvp.md`.

ID: PROSPECT-001
Title: Evaluate TurboQuant For Compressed Document-Vector Storage And Indexing
Status: Exploring
Target Stage Or Epic: Post-MVP research related to Epic 3, Embedding And Vector Indexing
Last Reviewed: 2026-07-29
Rationale: Google presents TurboQuant as an online vector-quantization method for reducing memory overhead in vector search. The project should determine whether it can reduce local storage and memory use for document embeddings without unacceptable retrieval or answer-quality loss.
Proposed Direction: Prototype compression of document embeddings before or during vector-index storage, evaluating multiple bit widths and whether compressed vectors can be queried directly or require dequantization or a custom index adapter. Keep SQLite as the canonical full-text chunk store and treat compressed Qdrant data as rebuildable experimental index data. Compare against the current uncompressed vector baseline.
Dependencies: A stable document ingestion and embedding/indexing pipeline; representative local evaluation datasets; a local TurboQuant implementation or reproducible prototype; Qdrant compatibility testing; retrieval and end-to-end answer-quality evaluation tooling.
Risks: TurboQuant may not be a drop-in Qdrant storage or query strategy and may require an adapter or custom vector-index path. Quantization distortion could reduce recall, citation correctness, or answer quality. Compression, dequantization, filtering, persistence, and recovery behavior may add latency or operational complexity.
Evidence: [Google Research: TurboQuant](https://research.google/blog/turboquant-redefining-ai-efficiency-with-extreme-compression/); [TurboQuant paper](https://arxiv.org/abs/2504.19874). The paper reports nearest-neighbor search experiments, but project-specific compatibility and quality impact remain unverified.
Resulting Decision: No architecture or roadmap decision yet; experiment required. Promotion, deferral, or rejection should follow a reproducible benchmark covering memory and disk reduction, index build and rebuild time, query latency, Recall@k or nDCG, result overlap, end-to-end answer quality, citation correctness, and Qdrant filtering, persistence, and recovery.

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
2. Update `docs/ROADMAP.md` or the relevant file under `docs/architecture/`.
3. Add an active entry to `docs/DECISIONS.md` when the approval changes architecture, tooling, models, workflow, or repository conventions.
4. Link the resulting decision from the prospect.
5. Merge the governance checkpoint into `main` before implementation starts.

Rejected and deferred prospects remain in this file so the reasoning is not lost.
