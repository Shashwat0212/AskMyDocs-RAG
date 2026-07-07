# Roadmap

The roadmap follows the Technical Design Document.

## Stage 0: Day Zero Foundation

Prepare repository structure, engineering workflow, documentation standards, AI-agent synchronization, and development environment guidance.

## Stage 1: Core RAG MVP

Build the first working document-based question-answering pipeline. The first Phase 1 epic focuses on backend framework familiarization, local service setup, and repeatable local tooling before product feature work begins:

- FastAPI, backend testing, configuration, and logging familiarization
- Flow-level tracing and local-first observability foundation
- Testable backend health endpoint
- Local Qdrant setup and verification
- Local Ollama setup and verification
- Common local operations commands and documentation

After the setup epic is complete, continue into the Core RAG MVP feature pipeline:

- Document upload API
- Text extraction
- Configurable and pluggable chunking
- Embedding generation
- Qdrant indexing
- Canonical local chunk storage with dense and lexical indexes
- Lightweight hybrid retrieval
- Answer generation
- Citation display
- Basic request and response logging
- Configuration-driven model and retrieval settings

After the MVP Gradio interface is working, continue with Phase 1 post-MVP enhancements:

- Optional local reranking for retrieval quality
- Session memory and conversation retrieval

Phase 1 planning for Epics 1 through 8 is captured in `docs/architecture/phase_1_core_rag_mvp.md`, with detailed lean MVP steps in `docs/architecture/phase_1_epic_steps.md`.

## Stage 2: Retrieval Inspection And Quality Layer

Add retrieval debugging, source inspection, and higher-quality generation:

- Retrieved chunk viewer
- Similarity score display
- Citation inspection panel
- Prompt and context preview
- Retrieval trace logging
- Quality mode using Qwen2.5 7B

## Stage 3: Documentation Automation

Build automated documentation update workflow from code changes:

- Changed-file detector
- FastAPI route-change detector
- Configuration and schema-change detector
- Documentation impact mapper
- Markdown patch generator
- Pull request comment or documentation artifact

## Stage 4: Evaluation Engine

Add automated RAG quality evaluation and regression tracking:

- Evaluation dataset format
- Local judge integration
- RAGAS metric pipeline
- DeepEval regression tests
- JSON evaluation output
- Static HTML/Markdown reports
- GitHub Pages publishing workflow

## Stage 5: Multi-Model Routing And Semantic Cache

Add model selection, response reuse, and cache-aware generation:

- Model selector
- Model routing layer
- Qdrant semantic cache collection
- Cache lookup pipeline
- Cache invalidation rules
- Cache hit/miss logging
- Cache inspection view

## Stage 6: Output Arbitration

Add a review layer for difficult, low-confidence, or high-risk responses:

- Arbitration router
- Critic prompt template
- Judge prompt template
- Structured arbitration output
- Retry or rewrite workflow
- Arbitration trace logging
- Arbitration result display in UI
