# AskMyDocs-RAG

AskMyDocs-RAG is a local-first RAGOps platform for document ingestion, retrieval, answer generation, evaluation, semantic caching, model routing, arbitration, and automated documentation updates.

This repository is currently in Day Zero foundation state. It contains project standards, documentation structure, AI-agent workflow guidance, placeholder subsystem folders, and example configuration files only. It intentionally does not contain backend code, frontend code, APIs, retrieval logic, evaluation logic, caching, database logic, or deployment pipelines yet.

## Project Constraints

- Use fully free and open-source/local-first components.
- Do not depend on paid LLM APIs, paid hosted inference, paid vector databases, paid evaluation services, or paid observability platforms.
- Prefer configuration over hardcoded values.
- Keep changes small, focused, documented, and reviewable.
- Update documentation whenever implementation changes.

## Target Stack

- Backend API: FastAPI
- MVP UI: Gradio
- Final UI: React / Next.js
- Model serving: Ollama first, llama.cpp for advanced local serving
- Vector store: Qdrant
- Main generation model: Qwen3 4B
- Quality generation model: Qwen2.5 7B Instruct
- Critic model: DeepSeek-R1-Distill-Qwen-7B
- Main embedding model: nomic-embed-text-v1.5
- Cache embedding model: bge-small-en-v1.5
- Evaluation frameworks: DeepEval and Ragas
- Local deployment: Docker Compose
- Static reports and documentation: GitHub Pages
- CI workflow: GitHub Actions

## Read First

Before starting any task, human engineers and AI coding assistants should read:

1. [AGENTS.md](AGENTS.md)
2. [docs/PROJECT_STATUS.md](docs/PROJECT_STATUS.md)
3. [docs/ROADMAP.md](docs/ROADMAP.md)
4. [docs/ENGINEERING_WORKFLOW.md](docs/ENGINEERING_WORKFLOW.md)
5. [docs/DEVELOPMENT_ENVIRONMENT.md](docs/DEVELOPMENT_ENVIRONMENT.md)
6. [docs/CODING_STANDARDS.md](docs/CODING_STANDARDS.md)
7. [docs/AI_AGENT_WORKFLOW.md](docs/AI_AGENT_WORKFLOW.md)

## Current State

Day Zero foundation is being established. The first feature ticket should start only after this scaffolding is reviewed and accepted.
