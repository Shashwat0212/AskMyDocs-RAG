# Epic 3 — Indexing And Retrieval

Tickets: `RAG-011`–`RAG-021`

Runtime: Free-tier Colab

Status: Planned

## Goal

Build and test the complete Qdrant retrieval path before creating the formal benchmark or calling an LLM.

## Tickets

- `RAG-011`: dense and sparse embedding interfaces that report model, version, dimension, and normalization metadata.
- `RAG-012`: Qdrant schema with named dense/sparse vectors, complete chunk text, stable IDs, and citation payloads.
- `RAG-013`: indexing flow and deterministic collection naming.
- `RAG-014`: rebuild, compatibility, payload, dimension, and indexing tests.
- `RAG-015`: retrieval service and API contracts, including trace and profile placeholders.
- `RAG-016`: dense Qdrant retrieval.
- `RAG-017`: Qdrant sparse/BM25 retrieval.
- `RAG-018`: native Qdrant fusion using RRF by default and configurable DBSF.
- `RAG-019`: configurable reranker interface and bounds.
- `RAG-020`: local `cross-encoder/ms-marco-MiniLM-L-6-v2` reranker with timeout and bypass behavior.
- `RAG-021`: dense, sparse, fusion, payload, reranking, fallback, and trace tests.

## Completion Criteria

- Collections can be rebuilt from source documents, manifests, and configuration.
- Qdrant returns complete chunks and citation metadata without a second chunk store.
- Dense and sparse candidates can be inspected separately.
- Fusion and reranking preserve score and trace provenance.
- Reranking is configurable, bypassable, bounded, and failure-tolerant.
- Compatibility failures are clear and do not silently query the wrong collection.

## Out Of Scope

Golden dataset construction, configuration selection, decision-tree navigation, answer generation, and UI behavior.
