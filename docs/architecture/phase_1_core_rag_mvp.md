# Phase 1 Core RAG MVP Plan

## Purpose

Phase 1 turns the Day Zero repository foundation into the first working local-first document question-answering application.

This plan covers Epics 1 through 7 only. It follows the project Technical Design Document and Approach document while adding a lightweight hybrid retrieval target for the MVP.

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

## Epic 1: Core Backend Foundation

Finished state:

- FastAPI backend exists and runs locally.
- Backend package structure supports API routes, configuration, logging, schemas, and future service modules.
- Configuration loads from environment variables and config file paths.
- Logging is initialized once and can be reused by later modules.
- Health endpoint verifies the backend process is running.
- Backend tests can run locally.

Representative tickets:

- `RAG-001`: Create FastAPI backend skeleton.
- `RAG-002`: Add backend configuration loading.
- `RAG-003`: Add structured logging foundation.
- `RAG-004`: Add health endpoint and tests.
- `RAG-005`: Document backend local run workflow.

Out of scope:

- Document upload.
- Qdrant calls.
- Ollama calls.
- Retrieval or generation logic.

## Epic 2: Local Service Infrastructure

Finished state:

- Qdrant can run locally through Docker Compose.
- Ollama setup expectations are documented as a local prerequisite.
- `.env.example` contains local service URLs and config path variables.
- Common local commands exist through Make or an equivalent task runner.
- Operations documentation explains how to start, stop, and verify local services.

Representative tickets:

- `RAG-006`: Add Docker Compose for Qdrant.
- `RAG-007`: Add local service environment variables.
- `RAG-008`: Add Makefile command conventions.
- `RAG-009`: Document Ollama and Qdrant local setup.
- `RAG-010`: Add lightweight service readiness checks if useful.

Out of scope:

- Production deployment.
- GitHub Actions deployment workflows.
- Bundling Ollama in Docker without explicit approval.

## Epic 3: Document Ingestion Pipeline

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

## Epic 4: Embedding And Vector Indexing

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

## Epic 5: Hybrid Retrieval Pipeline

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

## Epic 6: Answer Generation With Citations

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

## Epic 7: MVP Gradio Interface

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
