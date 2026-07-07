# Phase 1 Core RAG MVP Plan

## Purpose

Phase 1 turns the Day Zero repository foundation into the first working local-first document question-answering application.

This plan covers Epics 1 through 9. Epics 1 through 6 deliver the first lean MVP. Epics 7 through 9 are post-MVP retrieval, conversation-memory, and hyperparameter experimentation enhancements that should begin only after the MVP Gradio interface is working.

## Lean MVP Outcome

At the end of Epic 6, a local developer should be able to:

1. Start local services.
2. Start the FastAPI backend.
3. Upload a supported document.
4. Extract and chunk document text.
5. Index chunks into Qdrant.
6. Ask a question from the Gradio interface.
7. Retrieve relevant chunks using simple hybrid retrieval.
8. Generate an answer with citations using a local Ollama-served model.

Phase 1 must not introduce paid hosted services, deployment pipelines, semantic caching, model routing, arbitration, evaluation automation, or the final React/Next.js interface.

## Epic 1: Backend Foundations And Local Tooling Familiarization

Finished state:

- Developers understand the backend tools well enough to operate and extend them safely.
- FastAPI backend exists, runs locally, and has a testable health endpoint.
- Backend package structure supports API routes, configuration, logging, schemas, and future service modules.
- Configuration loads from environment variables and config file paths.
- Logging, flow-level tracing, and local-first observability foundations can be reused by later modules.
- Qdrant can run locally through Docker Compose and can be verified independently.
- Ollama setup expectations are documented as a local prerequisite and can be verified independently.
- Common local commands exist through Make or an equivalent task runner.
- Operations documentation explains how to start, stop, and verify local backend tooling.

Representative tickets:

- `RAG-001`: FastAPI And Backend Basics Learning Spike.
- `RAG-002`: Create Testable FastAPI Backend Skeleton.
- `RAG-003`: Add Backend Settings And Observability Foundation.
- `RAG-004`: Docker Compose And Qdrant Local Sandbox.
- `RAG-005`: Ollama Local Model Serving Sandbox.
- `RAG-006`: Local Backend Tooling And Operations Workflow.

Learning and setup expectations:

- Tutorial videos are learning aids for developer familiarity.
- Official project docs and official tool documentation remain the implementation source of truth.
- Sandbox experiments must be clearly separated from product feature code.

Out of scope:

- Document upload.
- Text extraction.
- Chunking.
- Embeddings.
- Backend Qdrant indexing or retrieval calls.
- Backend Ollama generation calls.
- Gradio interface.
- Production deployment or GitHub Actions deployment workflows.

Detailed step planning for Epics 1 through 6 is captured in `phase_1_epic_steps.md`.

## Epic 2: Document Ingestion Pipeline

Finished state:

- Backend exposes a document upload API.
- Supported file types are validated.
- Text is extracted from uploaded documents.
- Extracted text is split into chunks.
- Chunk metadata is created for source, document, page or section when available, and chunk ordering.
- Chunking is configuration-driven and supports pluggable strategies so chunking can be tuned as a RAG hyperparameter.
- Ingestion logic has focused unit tests.

Representative tickets:

- `RAG-011`: Add document upload API contract.
- `RAG-012`: Add file validation and storage boundary.
- `RAG-013`: Add text extraction pipeline.
- `RAG-014`: Add configurable chunking.
- `RAG-015`: Add ingestion metadata and tests.

Out of scope:

- Advanced parsing quality work.
- Retrieval trace UI.
- Evaluation datasets.

## Epic 3: Embedding And Vector Indexing

Finished state:

- Backend can generate document chunk embeddings using the configured local embedding model.
- Qdrant collection setup is configuration-driven.
- Document chunks are stored in a canonical local chunk store.
- Document chunk vectors and lightweight metadata are indexed into Qdrant.
- SQLite FTS or equivalent local lexical indexing can use the same canonical chunk text for later BM25 retrieval.
- Indexing can be tested without relying on paid services.

Representative tickets:

- `RAG-016`: Add local embedding client interface.
- `RAG-017`: Add Qdrant client and collection setup.
- `RAG-018`: Index chunk embeddings and metadata.
- `RAG-019`: Add indexing tests with local or mocked boundaries.

Out of scope:

- Semantic cache collection.
- Model routing.
- Reranker integration.

## Epic 4: Hybrid Retrieval Pipeline

Finished state:

- Backend accepts a user question for retrieval.
- Dense retrieval embeds the query and searches Qdrant.
- Lightweight lexical retrieval scores chunks using a local, free approach such as SQLite FTS5/BM25 over the canonical chunk store.
- Dense and lexical results are fused with configurable weights.
- Retrieval hydrates fused `chunk_id` results from the canonical chunk store and returns ranked chunks with source metadata and retrieval scores needed for citations.
- The retrieval mode is configuration-driven and defaults to hybrid for Phase 1.

Recommended Phase 1 retrieval shape:

- Dense retrieval: Qdrant vector search with `nomic-embed-text-v1.5`.
- Lexical retrieval: SQLite FTS5/BM25 or another local lexical strategy over canonical chunk text.
- Fusion: reciprocal rank fusion or weighted score fusion, selected in config.
- Controls: `top_k`, dense weight, lexical weight, score threshold, and retrieval mode.

Representative tickets:

- `RAG-020`: Add retrieval API contract.
- `RAG-021`: Add dense query embedding and Qdrant search.
- `RAG-022`: Add lightweight lexical retrieval.
- `RAG-023`: Add configurable result fusion.
- `RAG-024`: Add retrieval tests for dense, lexical, and hybrid paths.

Out of scope:

- Cross-encoder reranking.
- LLM-based reranking.
- Retrieval trace viewer.
- Prompt/context preview UI.
- Quality model mode.
- Session memory or conversation retrieval.

## Epic 5: Answer Generation With Citations

Finished state:

- Backend assembles retrieved chunks into prompt context.
- Prompt template is loaded from configuration.
- Generation uses the configured local Ollama model.
- Answer response includes citations mapped back to retrieved chunk metadata.
- Basic request, retrieval, and generation metadata are returned or logged.
- Answer generation is stateless or minimal-session for the first MVP and does not retrieve long-term conversation memory.

Representative tickets:

- `RAG-025`: Add prompt assembly from retrieved chunks.
- `RAG-026`: Add Ollama generation client.
- `RAG-027`: Add answer API with citation response.
- `RAG-028`: Add generation tests with mocked model boundary.

Out of scope:

- Multi-model routing.
- Critic or judge models.
- Arbitration workflow.
- Session memory retrieval.

## Epic 6: MVP Gradio Interface

Finished state:

- Gradio app allows document upload.
- Gradio app allows asking a question.
- UI displays answer text and citations.
- UI surfaces basic loading and error states.
- UI calls FastAPI endpoints and does not duplicate backend business logic.

Representative tickets:

- `RAG-029`: Add Gradio app skeleton.
- `RAG-030`: Add document upload flow.
- `RAG-031`: Add question-answer flow.
- `RAG-032`: Display citations and basic errors.
- `RAG-033`: Document MVP UI run workflow.

Out of scope:

- React/Next.js final interface.
- Retrieval inspection panels.
- Cache inspection views.
- Evaluation report views.
- Reranking controls.
- Session memory controls.

## Epic 7: Reranking And Retrieval Quality

Finished state:

- Hybrid retrieval can optionally rerank fused candidate chunks using a local reranking strategy.
- Reranking is disabled by default until validated.
- The default planned reranker is a local cross-encoder, not an LLM reranker.
- Retrieval output preserves pre-rerank dense, lexical, and fusion scores for debugging.
- Reranking behavior is configuration-driven and can be bypassed.
- Reranking tests cover ordering, disabled behavior, error handling, and latency-sensitive paths.

Recommended post-MVP reranking shape:

- Input: top fused retrieval candidates from Epic 4.
- Default approach: local cross-encoder reranker.
- Future option: LLM reranking only if explicitly approved after latency and quality review.
- Controls: enabled flag, provider, model, rerank input size, final output size, timeout, and fallback behavior.

Representative tickets:

- `RAG-034`: Add reranking configuration and interface.
- `RAG-035`: Add local cross-encoder reranker implementation.
- `RAG-036`: Integrate optional reranking after hybrid fusion.
- `RAG-037`: Add reranking tests and retrieval quality documentation.

Out of scope:

- Hosted reranking APIs.
- LLM reranking as the first/default path.
- Retrieval inspection UI.
- Evaluation automation.
- Model routing.

## Epic 8: Session Memory And Conversation Retrieval

Finished state:

- Chat/session history can be stored locally without mixing it into the document corpus.
- Full chat text is stored cheaply in SQLite or equivalent local storage.
- Session memory indexes are separate from document indexes.
- Relevant session memory can be retrieved for a session-aware answer.
- Prompt assembly can include bounded session context using context caps, recent turns, summaries, and retrieved memory chunks.
- Parent-child memory retrieval is supported conceptually: retrieve smaller memory chunks, then hydrate parent messages or summaries when needed.

Recommended post-MVP session memory shape:

- Document indexes and session memory indexes remain separate.
- Canonical chat storage uses local SQLite tables for sessions, messages, memory chunks, and summaries.
- Session memory retrieval may use separate Qdrant collection or namespace plus SQLite FTS/BM25.
- Context budgeting prioritizes current question, system instructions, retrieved document chunks, highly relevant session memory, recent turns, and older summaries.
- Session memory retrieval should be configurable and can be disabled until quality is validated.

Representative tickets:

- `RAG-038`: Add local session and chat message storage.
- `RAG-039`: Add session memory chunking and summary storage.
- `RAG-040`: Add separate session memory retrieval indexes.
- `RAG-041`: Integrate bounded session context into answer prompt assembly.
- `RAG-042`: Add session memory tests and documentation.

Out of scope:

- Mixing chat memory into the document corpus.
- Passing full conversation history into every prompt.
- Hosted memory stores.
- Semantic cache implementation.
- Multi-model routing.

## Epic 9: Hyperparameter Experimentation And Blueprinting

Finished state:

- A local experimentation module can run configured RAG pipeline permutations over one or more evaluation datasets.
- Experiment inputs are driven by configuration rather than hardcoded combinations.
- The module can vary approved hyperparameters across chunking, embedding/indexing settings, retrieval, fusion, reranking, prompt settings, generation settings, and session-memory settings where available.
- Each experiment run records the exact configuration, dataset, metrics, latency, errors, and output artifacts needed to compare results.
- Results identify which configurations performed better for a given dataset.
- Multi-dataset comparisons can be used to build a practical blueprint of which hyperparameter patterns work better for different document quality levels, industries, and use cases.

Recommended post-MVP experimentation shape:

- Treat the implemented config files as the control plane for experiments.
- Define named experiment profiles that expand into specific permutations.
- Keep dataset definitions local under the evaluation area.
- Use existing evaluation frameworks from the roadmap, such as DeepEval and Ragas, when the evaluation stage is implemented.
- Store experiment outputs locally as structured files and later render static reports.
- Keep the first implementation focused on repeatable offline experiments, not automatic production tuning.

Candidate hyperparameter families:

- Chunking strategy, chunk size, chunk overlap, and metadata strategy.
- Embedding model, vector dimensions, and indexing options.
- Retrieval mode, dense top-k, lexical top-k, score thresholds, and fusion strategy.
- Reranking enabled flag, reranker model, rerank input size, and final output size.
- Prompt template, context budget, and citation formatting rules.
- Generation model, temperature, max tokens, timeout, and stop rules.
- Session memory context cap, recent-turn count, summary strategy, and memory retrieval limits.

Representative tickets:

- `RAG-043`: Define experiment configuration schema and run manifest.
- `RAG-044`: Add local experiment runner for configured pipeline permutations.
- `RAG-045`: Add dataset registry and dataset quality/industry metadata.
- `RAG-046`: Capture experiment metrics, latency, errors, and artifacts.
- `RAG-047`: Add comparison report generation for experiment runs.
- `RAG-048`: Document hyperparameter blueprinting workflow.

Out of scope:

- Paid or hosted experiment tracking platforms.
- Automatic online tuning in production.
- Changing production defaults without explicit review.
- Replacing the approved local-first evaluation direction.
- Running experiments before the underlying pipeline modules exist.

## Phase 1 Acceptance Criteria

Phase 1 is complete when:

- Local services can be started.
- Backend health check passes.
- A supported document can be uploaded.
- Text is extracted, chunked, embedded, and indexed.
- A question retrieves chunks through hybrid retrieval.
- A local model generates an answer.
- Citations are shown in the API response and Gradio UI.
- Configuration controls model names, service URLs, retrieval settings, prompt paths, and experimentable pipeline parameters.
- Relevant tests pass or any local environment limitation is documented.
- Documentation for setup, configuration, APIs, and operations is updated.

The first MVP is complete after Epic 6. Epics 7 through 9 should be treated as post-MVP Phase 1 enhancement work.

## Future Epics Remain In Roadmap

The remaining broader roadmap areas stay outside Phase 1:

- Retrieval inspection UI and broader quality-mode layer.
- Documentation automation.
- Evaluation engine.
- Multi-model routing and semantic cache.
- Output arbitration.
- Final React/Next.js interface.

Those areas should not be implemented during Phase 1 unless the project owner explicitly changes the approved scope.
