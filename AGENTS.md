# AI Agent Instructions — Project Governance

This file governs AI assistants working on the `project-governance` branch.

## Start Every Run

1. Read `START_HERE.md`.
2. Read this file.
3. Read the task-specific governance documents linked from
   `governance/README.md`.
4. Inspect the branch and preserve unrelated user changes.

## Authority

The owner-provided documents under `governance/sources/` define the original
project intent. Later project-owner approvals recorded in
`governance/decisions/DECISIONS.md` are explicit amendments and may supersede
older planning details while preserving the source documents unchanged.

## Branch Purpose

This branch contains governance documents only. Do not add application code,
runtime configuration, deployment files, notebooks, generated datasets, or
evaluation implementations here.

## Required Behavior

- Keep status, roadmap, epic plans, decisions, and handoff records consistent.
- Keep changes small and reviewable.
- Prefer clear language and avoid repeating the same plan in several files.
- Record approved changes in the decision log.
- Update `START_HERE.md` when the current phase, active epic, next work, or
  approved sequence changes.
- Preserve the governing DOCX files unless the project owner explicitly asks
  to revise them.
- Never merge this branch wholesale into `main`.
- Promote only approved, implementation-facing guidance through a documented
  handoff.

## Branches And Implementation

- `main` remains the approved implementation baseline.
- Epic branches start from `main` and use `epic/<epic-id>-short-description`.
- Ticket branches start from the active epic branch and use
  `feature/<developer>/<ticket-id>-short-description`.
- Product code, tests, runtime documentation, and implementation-level
  `KNOWLEDGE.md` updates happen on ticket and epic branches, not here.

## Before Completing Governance Work

- Check links and file paths.
- Confirm ticket IDs and epic numbering are consistent.
- Confirm current status and roadmap agree.
- Confirm new decisions identify what they supersede.
- Run `git diff --check`.
- Summarize changed plans, validation, and any handoff required.
