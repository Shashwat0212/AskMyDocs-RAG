# Sandbox Knowledge

## Current Contents

The `sandbox/` area contains ticket-scoped learning environments that are kept
separate from product code. The first sandbox is the RAG-002 Qdrant music
tutorial under `qdrant_music/`.

## Boundary

Sandbox packages may demonstrate approved local tools, but the backend and
frontend must not import them. Reusable product integrations belong in their
later implementation epics.

## Update Notes

Update this file and the root `KNOWLEDGE.md` map whenever a sandbox is added,
removed, or changes responsibility.
