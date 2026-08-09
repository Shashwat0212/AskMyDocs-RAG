# AskMyDocs-RAG Project Governance

This branch is the planning workspace for AskMyDocs-RAG. It contains project
status, roadmap, decisions, engineering rules, Phase 1 epic plans, source
documents, and approved handoff records. It intentionally contains no
application code or application placeholder folders.

Start with [START_HERE.md](START_HERE.md), then read [AGENTS.md](AGENTS.md).
The complete navigation index is [governance/README.md](governance/README.md).

## Branch Boundary

- `project-governance` is never merged wholesale into `main`.
- Application work happens on ticket branches created from the active epic
  integration branch.
- Approved planning is promoted through a small handoff that records the
  governance commit, target branch, scope, and acceptance criteria.
- Implementation results are recorded back here by commit reference, without
  merging implementation history into this branch.

## Phase 1 Direction

Phase 1 has seven epics. Retrieval is implemented before evaluation; the
retrieval benchmark is built before configuration experiments; validated
profiles and decision-tree navigators are selected before answer generation
and the local Gradio MVP.

The project remains local-first, free and open-source, configuration-driven,
and independent of paid hosted AI, vector database, evaluation, or
observability services.
