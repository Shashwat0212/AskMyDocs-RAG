# Epic 6 — Answer Generation

Tickets: `RAG-038`–`RAG-041`

Runtime: Free-tier Colab

Status: Planned

## Goal

Generate cited answers from navigator-selected evidence while keeping model behavior behind a stable, local adapter.

## Tickets

- `RAG-038`: bounded prompt assembly using retrieved chunks, selected profile IDs, and configuration-managed templates.
- `RAG-039`: pinned self-managed Ollama runtime in Colab and generation client adapter.
- `RAG-040`: answer API returning text, citations, trace ID, ingestion/query profile provenance, and fallback state.
- `RAG-041`: prompt, citation, insufficient-context, timeout, runtime-failure, navigator-integration, and mocked-boundary tests.

## Completion Criteria

- Prompt assembly uses only the bounded chunks returned by retrieval.
- Citation identifiers map back to source metadata.
- Responses expose trace and profile provenance.
- Insufficient context produces a stable abstention response.
- Ollama timeouts and failures do not create unsupported answers.
- Model infrastructure remains replaceable without changing retrieval business logic.

## Evaluation Boundary

Phase 1 tests context construction, citation mapping, abstention, provenance, and model-boundary failures. It does not use model-dependent coherence to judge retrieval quality or claim one LLM is universally best.

Ragas, DeepEval, LLM-as-judge scoring, prompt comparison, and broad answer-quality benchmarking remain in the later Generation and System Evaluation stage.
