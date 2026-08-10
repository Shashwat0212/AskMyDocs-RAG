# Qdrant Music Sandbox Knowledge

## Purpose

This directory is the isolated RAG-002 learning environment for Qdrant. It uses
a frozen Billboard Hot 100 top-50 snapshot and locally generated Nomic
embeddings to demonstrate collections, points, payloads, exact search, HNSW,
filtering, indexing, updates, deletion, persistence, and inspection.

## Structure

- `src/qdrant_music/` contains shared settings, dataset validation, embedding,
  Qdrant operations, and the CLI.
- `src/qdrant_music/tutorial_steps/` contains small phase-aligned programs.
- `fixtures/` contains the immutable chart snapshot and provenance notice.
- `tests/` validates the dataset, configuration, phase synchronization, and
  logic that does not require a running Qdrant service.
- `pyproject.toml` and `uv.lock` define the isolated Python environment.

## Boundary

This package is educational. The FastAPI backend must not import it. Product
embedding and Qdrant client abstractions remain work for later epics.

## Update Notes

When a tutorial phase changes, update the Markdown walkthrough, matching Python
step, Jupyter section, tests, and relevant knowledge documents together.
