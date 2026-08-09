# Epic 4 — Retrieval Evaluation

Tickets: `RAG-022`–`RAG-028`

Runtime: Free-tier Colab

Status: Planned

## Goal

Build a human-approved benchmark that measures how well the engineered retrieval pipeline finds evidence across document types, corpus sizes, and distractor variations.

## Corpus Matrix

Use three public, safely redistributable document families:

- Financial and regulatory documents.
- Technical manuals and documentation.
- Policy and procedural documents.

Build three nested text-size tiers for each family:

| Tier | Target extracted tokens | Allowed tolerance |
|---|---:|---:|
| Small | 10,000 | ±10% |
| Medium | 1,000,000 | ±10% |
| Large | 100,000,000 | ±10% |

Create five deterministic variants at every family and size. Each variant keeps the gold evidence documents fixed and changes the seeded distractor/background documents.

```text
3 document families × 3 sizes × 5 variants = 45 corpus instances
```

Do not reach a token target by repeating identical text. Large runs may be slow, but must be checkpointable and resumable. Documented free-tier failures remain visible evidence.

## Golden Questions

Create 100 approved questions per family, for 300 total.

For each family:

- 60 scale-invariant questions:
  - 45 answerable from the smallest tier onward.
  - 15 unanswerable or distractor-heavy.
- 20 questions whose evidence first appears in the medium tier.
- 20 questions whose evidence first appears in the large tier.

Across the 85 answerable questions in each family:

- 40 are direct single-evidence questions.
- 25 require multiple pieces of evidence.
- 20 use paraphrased or domain-specific wording.

Use 70 development and 30 locked-holdout questions per family. Split by source document and keep the categories and size tiers balanced. Epic 5 may tune only on the 210 development questions. The 90 holdout questions are opened only for final profile promotion.

## Codex And Human Review

Codex may draft the question, expected answer, answerability label, category, and supporting evidence. Every field must be reviewed by a human.

Records use these states:

```text
draft → reviewed → approved
```

Only `approved` records enter benchmark scoring. Approval stores the reviewer, timestamp, annotation version, and corpus version.

## Evidence Format

Chunk IDs are not canonical gold labels because chunking experiments change them. Store stable source evidence instead:

- Corpus and document IDs.
- Page or section.
- Exact normalized supporting span.
- Evidence hash.
- Required or acceptable-alternative status.
- Graded relevance.
- Multi-evidence group where applicable.

For each experiment, map generated chunks back to approved evidence spans and derive the relevant chunk IDs for that run.

## Retrieval Approaches

Establish four baselines:

1. Dense retrieval only.
2. Sparse/BM25 retrieval only.
3. Hybrid dense and sparse retrieval.
4. Hybrid retrieval followed by reranking.

## Metrics

- Dense and sparse candidate stages: Recall@20.
- Fusion stage: Recall@10 and nDCG@10.
- Final reranked output: evidence Recall@5, Precision@5, nDCG@5, and MRR@5.
- Multi-evidence questions: complete evidence-set coverage@5.
- Unanswerable questions: false-positive behavior under configured thresholds.
- Runtime: P50/P95 query latency, failures, and timeout rate.

Metrics must be calculated deterministically and tested against hand-computed fixtures.

## Tickets

- `RAG-022`: corpus registry, licenses, checksums, nested size manifests, and five seeded variants per tier.
- `RAG-023`: golden-record schema and Codex-assisted draft generation.
- `RAG-024`: human review workflow, approval states, split rules, and dataset validation.
- `RAG-025`: stable evidence-anchor to generated-chunk mapping.
- `RAG-026`: checkpointed retrieval runner and deterministic metric calculations.
- `RAG-027`: execute and report the four baseline approaches.
- `RAG-028`: approve benchmark baselines, regression rules, and the Epic 5 handoff.

## Completion Criteria

- All 45 corpus manifests are reproducible from checksums and seeds.
- All 300 questions are human-approved.
- Development and holdout source documents do not overlap.
- Evidence maps correctly across supported chunking profiles.
- All four retrieval baselines run on the required benchmark slices.
- Large-tier work resumes safely after interruption.
- Reports separate retrieval stages, corpus families, sizes, variants, and query categories.
- Results are described as benchmark evidence, never “GPT-level retrieval.”

## Out Of Scope

Configuration search, profile promotion, navigator training, answer generation, and LLM-as-judge evaluation.
