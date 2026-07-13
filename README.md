# AskMyDocs-RAG

AskMyDocs-RAG is a local-first RAGOps platform for document ingestion, retrieval, answer generation, evaluation, semantic caching, model routing, arbitration, and automated documentation updates.

This repository has completed its Day Zero foundation and is entering Phase 1 planning. It currently contains project standards, documentation structure, AI-agent workflow guidance, placeholder subsystem folders, and example configuration files only. It intentionally does not contain backend code, frontend code, APIs, retrieval logic, evaluation logic, caching, database logic, or deployment pipelines yet.

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

1. [starter.md](starter.md)
2. [AGENTS.md](AGENTS.md)

Then use the task-routing table in `starter.md` to read the detailed sources required for the current task.

## Current State

Day Zero foundation has been reviewed and merged. Phase 1 is in planning, beginning with the Backend Foundations And Local Tooling Familiarization epic. The permanent `project-governance` branch contains the latest working project view; `main` contains the latest approved governance checkpoint. Create and approve the relevant Jira ticket before starting implementation.
