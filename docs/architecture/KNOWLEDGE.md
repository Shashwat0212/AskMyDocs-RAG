# Architecture Documentation Knowledge

## Current Contents

This folder contains architecture documentation and staged implementation planning. `phase_1_core_rag_mvp.md` defines seven Phase 1 epics and 41 sequential ticket references; `phase_1_epic_steps.md` expands their delivery flow. Epic 1 is local, Epics 2–6 are Colab-first, and Epic 7 returns local for the Gradio MVP. Qdrant owns Phase 1 dense/sparse retrieval, payloads, fusion, and citations; reranking is in Epic 4, experimentation/navigation is in Epic 5, and session memory is outside Phase 1.

## Responsibilities

Architecture docs define module boundaries, staged scope, runtime and persistence boundaries, configuration contracts, and planned implementation direction. They must remain aligned with the owner-provided source documents in `docs/source_documents/`.

## Update Notes

Update this file when architecture documents are added, renamed, or materially changed. Record major architecture decisions in `docs/DECISIONS.md`.
