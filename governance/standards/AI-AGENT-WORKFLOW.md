# AI-Agent Workflow

## Governance Work

1. Read `START_HERE.md`, `AGENTS.md`, and the relevant governance files.
2. Check current branch state and preserve unrelated changes.
3. Read both source DOCX files before changing architecture, stack, constraints, or stage order.
4. Treat later owner-approved decision entries as amendments to the source documents.
5. Update status, roadmap, epic plans, decisions, and handoffs together when affected.
6. Validate links, ticket numbering, and consistency before finishing.

AI agents must not add application code, runtime configuration, datasets, generated benchmark records, or deployment files to `project-governance`.

## Implementation Work

Implementation agents work on ticket branches and follow the handoff’s exact scope and acceptance criteria. They inspect existing code before editing, keep notebook logic thin, add tests, and update affected implementation documentation and `KNOWLEDGE.md` files.

## Codex-Assisted Golden Data

Codex may create draft questions, expected answers, categories, answerability labels, and evidence suggestions. Drafts are not gold data. A human must approve every field before a record can be scored.

Agents must not expose locked-holdout questions during profile tuning or use corpus-family labels as navigator training features.

## Completion Summary

Every completed task reports:

- What changed.
- Tests or checks performed.
- Documentation updated.
- Known limitations or blocked follow-up.
- Relevant governance, ticket, branch, and artifact references.
