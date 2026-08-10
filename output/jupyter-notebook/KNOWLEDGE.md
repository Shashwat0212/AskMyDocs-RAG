# Jupyter Notebook Knowledge

## Current Contents

`qdrant_billboard_internals_tutorial.ipynb` is the clean, restartable companion
to the RAG-002 Markdown walkthrough. It uses the shared sandbox package and
notebook-specific Qdrant collections.

`README.md` documents environment setup, kernel installation, execution,
validation, and cleanup.

## Synchronization Contract

The notebook uses phase IDs Q00 through Q16. Any behavioral tutorial change
must update the matching Markdown phase, Python step, notebook section, shared
configuration, tests, and knowledge documents.

## Output Policy

The committed notebook has no execution counts or stored outputs. Validate an
executed copy under `tmp/jupyter-notebook/`, then keep that path untracked.
