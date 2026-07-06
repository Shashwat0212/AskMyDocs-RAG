# Phase 1 Core RAG MVP Plan

## Purpose

Phase 1 turns the Day Zero repository foundation into the first working local-first document question-answering application.

This plan covers Epics 1 through 6 only. It follows the project Technical Design Document and Approach document while adding a lightweight hybrid retrieval target for the MVP.

## Phase 1 Outcome

At the end of Phase 1, a local developer should be able to:

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
- Logging is initialized once and can be reused by later modules.
- Qdrant can run locally through Docker Compose and can be verified independently.
- Ollama setup expectations are documented as a local prerequisite and can be verified independently.
- Common local commands exist through Make or an equivalent task runner.
- Operations documentation explains how to start, stop, and verify local backend tooling.

Representative tickets:

- `RAG-001`: FastAPI And Backend Basics Learning Spike.
- `RAG-002`: Create Testable FastAPI Backend Skeleton.
- `RAG-003`: Add Backend Settings And Logging Foundation.
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

## Epic 2: Document Ingestion Pipeline

Finished state:

- Backend exposes a document upload API.
- Supported file types are validated.
- Text is extracted from uploaded documents.
- Extracted text is split into chunks.
- Chunk metadata is created for source, document, page or section when available, and chunk ordering.
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
- Document chunks and metadata are indexed into Qdrant.
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
- Lightweight lexical retrieval scores chunks using a local, free, in-process approach.
- Dense and lexical results are fused with configurable weights.
- Retrieval returns ranked chunks with source metadata and retrieval scores needed for citations.
- The retrieval mode is configuration-driven and defaults to hybrid for Phase 1.

Recommended Phase 1 retrieval shape:

- Dense retrieval: Qdrant vector search with `nomic-embed-text-v1.5`.
- Lexical retrieval: simple local BM25 or term-based scoring over indexed chunk text or stored chunk payloads.
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
- Retrieval trace viewer.
- Prompt/context preview UI.
- Quality model mode.

## Epic 5: Answer Generation With Citations

Finished state:

- Backend assembles retrieved chunks into prompt context.
- Prompt template is loaded from configuration.
- Generation uses the configured local Ollama model.
- Answer response includes citations mapped back to retrieved chunk metadata.
- Basic request, retrieval, and generation metadata are returned or logged.

Representative tickets:

- `RAG-025`: Add prompt assembly from retrieved chunks.
- `RAG-026`: Add Ollama generation client.
- `RAG-027`: Add answer API with citation response.
- `RAG-028`: Add generation tests with mocked model boundary.

Out of scope:

- Multi-model routing.
- Critic or judge models.
- Arbitration workflow.

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

## Phase 1 Acceptance Criteria

Phase 1 is complete when:

- Local services can be started.
- Backend health check passes.
- A supported document can be uploaded.
- Text is extracted, chunked, embedded, and indexed.
- A question retrieves chunks through hybrid retrieval.
- A local model generates an answer.
- Citations are shown in the API response and Gradio UI.
- Configuration controls model names, service URLs, retrieval settings, and prompt paths.
- Relevant tests pass or any local environment limitation is documented.
- Documentation for setup, configuration, APIs, and operations is updated.

## Future Epics Remain In Roadmap

The remaining roadmap epics stay outside Phase 1:

- Retrieval inspection and quality layer.
- Documentation automation.
- Evaluation engine.
- Multi-model routing and semantic cache.
- Output arbitration.
- Final React/Next.js interface.

Those areas should not be implemented during Phase 1 unless the project owner explicitly changes the approved scope.
