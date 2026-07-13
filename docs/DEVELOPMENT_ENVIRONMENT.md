# Development Environment

This project is local-first. Developers should be able to run project services locally without paid hosted infrastructure.

## Required Software

- Git
- Docker Desktop or Docker Engine with Docker Compose
- Python 3.11
- Node.js LTS
- `pnpm`
- `uv` for Python environment management
- Ollama
- Make or an equivalent task runner

## Local Services

Stage 1 will use:

- Qdrant for vector storage
- Ollama for local model serving

Day Zero does not include Docker Compose files or service startup scripts. Those should be added in an approved setup ticket.

## Future Local Models

- Main generation: `qwen3:4b`
- Quality generation: Qwen2.5 7B Instruct
- Reasoning critic: DeepSeek-R1-Distill-Qwen-7B
- Main embeddings: nomic-embed-text-v1.5
- Cache embeddings: bge-small-en-v1.5
- Initial reranker: cross-encoder/ms-marco-MiniLM-L-6-v2
- Advanced reranker: bge-reranker-v2-m3

## Environment Variables

Use `.env.example` as the shared reference for local environment names. Do not commit `.env` files.

Environment variables should be used for:

- Local app environment
- Logging level
- Ollama base URL
- Qdrant URL
- Model names
- Config file paths

## Package Managers

- Python: prefer `uv` for reproducible environments.
- Python fallback: `python -m venv` and `pip`.
- Node: prefer `pnpm`.

Do not install backend or frontend dependencies until the related setup ticket is approved.

## Command Conventions

Common commands should eventually be exposed through a Makefile or equivalent task runner. Day Zero documents the expectation only and does not add executable project commands.
