# Architecture Documentation Knowledge

## Current Contents

This folder contains architecture documentation and staged implementation planning. The current Phase 1 Core RAG MVP plan is documented in `phase_1_core_rag_mvp.md`, with detailed lean MVP steps in `phase_1_epic_steps.md`. Backend foundation and local service setup are merged into a four-ticket setup-and-learning epic: one combined FastAPI ticket plus separate Qdrant, Ollama, and operations tickets. Reranking, session memory, and hyperparameter experimentation remain post-MVP enhancement epics.

## Responsibilities

Architecture docs define module boundaries, staged scope, important design constraints, and planned implementation direction. They must remain aligned with the owner-provided source documents in `docs/source_documents/`.

## Update Notes

Update this file when architecture documents are added, renamed, or materially changed. Record major architecture decisions in `docs/DECISIONS.md`.
