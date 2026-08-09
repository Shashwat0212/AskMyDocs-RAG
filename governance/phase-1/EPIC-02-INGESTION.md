# Epic 2 — Document Ingestion

Tickets: `RAG-005`–`RAG-010`

Runtime: Free-tier Colab

Status: Planned

## Goal

Turn supported documents into stable, citation-aware chunks through reusable package code.

## Tickets

- `RAG-005`: reproducible Colab bootstrap, branch checkout, pinned dependencies, Drive mount, and runtime diagnostics.
- `RAG-006`: document-upload API and stable response/error contracts.
- `RAG-007`: file validation and the Colab runtime/Drive storage boundary.
- `RAG-008`: PDF, TXT, and Markdown extraction with page or section metadata where available.
- `RAG-009`: configuration-driven chunking strategies with explicit size and overlap.
- `RAG-010`: stable document/chunk IDs, metadata contracts, and ingestion tests.

## Completion Criteria

- A fresh Colab runtime can reproduce the environment from pinned project inputs.
- Supported documents produce stable chunks with source and citation metadata.
- Working files stay on the Colab runtime; declared durable inputs and artifacts use Drive.
- Notebooks call importable package code and do not contain the business logic.
- Validation, extraction, chunking, metadata, and bootstrap tests pass.

## Out Of Scope

Embeddings, Qdrant indexing, retrieval, evaluation, generation, and UI behavior.
