# Configuration

This folder contains reviewed example configuration for models, retrieval, prompts, and evaluation. Examples do not create runtime behavior by themselves and contain no secrets.

Phase 1 uses three contracts:

- **Ingestion/index profile:** parser, chunker, embedding models/dimensions, Qdrant collection/index settings, and payload schema.
- **Query profile:** candidate limits, filters, fusion, thresholds, reranker, fallbacks, and output count.
- **Run manifest:** source commit, dataset/checksum, runtime, profile hash, Qdrant/model versions, metrics, errors, state, and artifact locations.

Selected compact profiles and summaries return to Git. Full experiment artifacts belong in configured shared Drive storage. Live Qdrant data belongs on the Colab runtime filesystem during Epics 2–6 and must never be written directly to mounted Drive.

Copy examples to ignored runtime files only when the owning ticket introduces the loader/schema. Prefer profiles over hardcoded values and never change a selected default without versioned benchmark evidence and review.
