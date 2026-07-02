# Day Zero Setup Playbook

This playbook is the onboarding source of truth for preparing a developer machine for AskMyDocs-RAG. It is written for engineers using Codex, Claude, GitHub Copilot, Cursor, Windsurf, other assistants, or no AI assistant at all.

AI is optional. It can help with inspection, validation, and repetitive setup work, but it is not required to contribute. The engineer remains responsible for understanding the project, reviewing generated output, testing changes, updating documentation, and staying within the assigned Jira ticket.

## Purpose

Day Zero exists to make every developer start from the same baseline before feature work begins.

The goal is not to build application features. The goal is to prepare:

- A consistent local development machine.
- A verified repository checkout.
- A Python virtual environment.
- Shared engineering and documentation standards.
- A common workflow for human-only and AI-assisted development.

Do not implement backend code, frontend code, APIs, retrieval logic, database logic, evaluation logic, caching, deployment pipelines, or model downloads during Day Zero unless a later ticket explicitly approves that work.

## Project Constraints

The project follows the Technical Design Document and Approach document.

- Local-first only.
- Free and open-source components only.
- No paid LLM APIs.
- No paid hosted inference.
- No paid vector databases.
- No paid evaluation services.
- No paid observability platforms.
- Prefer configuration over hardcoded values.
- Keep changes small and reviewable.
- Update documentation whenever implementation changes.

## Recommended Machine

Minimum workable machine:

- macOS, Linux, or Windows with WSL2.
- 16 GB RAM.
- 4 CPU cores.
- 25 GB free disk space for tooling, containers, and initial models.

Recommended for local model work:

- Apple Silicon Mac, modern Linux workstation, or Windows machine with WSL2.
- 32 GB RAM or more.
- 8+ CPU cores.
- 100 GB free disk space.
- GPU acceleration where available.

The verified setup in this project was performed on macOS Apple Silicon.

## Phase A: Machine Setup

Install only missing tools. Do not reinstall working tools.

### Required Tools

| Tool | Recommended version | Why it is needed | Verification command |
|---|---|---|---|
| Homebrew | Current stable on macOS | Installs developer tools consistently | `brew --version` |
| Git | 2.40+ | Source control and branch workflow | `git --version` |
| Python | 3.11.x | Backend and ML ecosystem baseline | `python3.11 --version` |
| pip | Bundled with Python 3.11 | Python package tooling | `python3.11 -m pip --version` |
| venv | Bundled with Python 3.11 | Local virtual environments | `python3.11 -m venv --help` |
| uv | Current stable | Preferred Python environment/package workflow | `uv --version` |
| Node.js | Active LTS, currently Node 24 | Future React/Next.js work | `node --version` |
| npm | Bundled with Node LTS | Node package tooling | `npm --version` |
| pnpm | Current stable | Preferred future frontend package manager | `pnpm --version` |
| Docker Desktop | Current stable | Local containers and future Qdrant service | `docker --version` |
| Docker Compose | Bundled with Docker Desktop | Local service orchestration | `docker compose version` |
| Ollama | Current stable | Local model serving | `ollama --version` |
| curl | System or current stable | HTTP checks and API validation | `curl --version` |
| wget | Current stable | CLI downloads | `wget --version` |
| make | System make is acceptable | Common command runner | `make --version` |
| jq | 1.7+ | JSON inspection and API checks | `jq --version` |
| unzip | System unzip is acceptable | Archive handling | `unzip -v` |

### macOS Installation Commands

Use these commands only for missing or non-compliant tools.

```bash
brew install python@3.11
brew install uv
brew install node@24
brew unlink node
brew link node@24 --force --overwrite
brew install --cask docker
brew install ollama
brew install wget
```

After installing Docker Desktop, open the Docker app once and wait for it to finish startup.

```bash
open -a Docker
```

If Docker was installed manually, verify that Docker Desktop created the CLI plugin directory and the `desktop-linux` context.

```bash
docker context ls
docker compose version
docker --context desktop-linux info
```

If Ollama is installed but not running, start it manually:

```bash
ollama serve
```

or start it as a background service:

```bash
brew services start ollama
```

Do not pull models during Day Zero unless explicitly approved.

## Phase B: Project Setup

Clone the repository and enter it.

```bash
git clone <repository-url>
cd AskMyDocs-RAG
```

Inspect the current state.

```bash
git status --short --branch
rg --files --hidden -g '!**/.git/**'
```

Confirm the Day Zero structure exists:

```text
AGENTS.md
CLAUDE.md
CODEX.md
.github/
backend/
configs/
deployment/
docs/
evals/
frontend/
README.md
.env.example
.editorconfig
.gitignore
```

Create a Python virtual environment only if one does not already exist.

```bash
python3.11 -m venv .venv
```

Verify the virtual environment directly:

```bash
.venv/bin/python --version
.venv/bin/python -m pip --version
```

Do not install project dependencies unless the dependency list has been reviewed and approved. At Day Zero, this repository intentionally has no `pyproject.toml`, `requirements.txt`, `package.json`, lockfiles, or Docker Compose file.

Check for dependency and service manifests:

```bash
find . -maxdepth 3 -type f \( -name 'pyproject.toml' -o -name 'requirements*.txt' -o -name 'package.json' -o -name 'pnpm-lock.yaml' -o -name 'package-lock.json' \)
find . -maxdepth 3 -type f \( -name 'docker-compose.yml' -o -name 'docker-compose.yaml' -o -name 'compose.yml' -o -name 'compose.yaml' \)
```

Expected Day Zero result: no dependency manifests and no Compose file.

## Environment Configuration

Use `.env.example` as the reference for environment variable names. Do not commit `.env`.

Current Day Zero variables:

```text
APP_ENV
LOG_LEVEL
OLLAMA_BASE_URL
MAIN_GENERATION_MODEL
QUALITY_GENERATION_MODEL
CRITIC_MODEL
MAIN_EMBEDDING_MODEL
CACHE_EMBEDDING_MODEL
QDRANT_URL
QDRANT_COLLECTION
QDRANT_CACHE_COLLECTION
MODELS_CONFIG_PATH
RETRIEVAL_CONFIG_PATH
PROMPTS_CONFIG_PATH
EVALUATION_CONFIG_PATH
```

Do not create runtime config files such as `configs/models.yaml` or `.env` unless a setup ticket approves that step. The current files under `configs/` are examples only.

## Local Services

Required future services:

- Ollama for local model serving.
- Qdrant for vector storage.

Current Day Zero service state:

- Ollama should be installed and reachable.
- Qdrant is not yet configured because the repository intentionally has no Docker Compose file.

Validate Ollama:

```bash
ollama list
curl http://localhost:11434/api/tags
```

Expected output with no models installed:

```text
NAME    ID    SIZE    MODIFIED
```

```json
{"models":[]}
```

Do not pull models unless approved. Required future models are identified in docs and config examples:

- `qwen3:4b`
- `qwen2.5:7b-instruct`
- `deepseek-r1-distill-qwen:7b`
- `nomic-embed-text-v1.5`
- `bge-small-en-v1.5`
- `cross-encoder/ms-marco-MiniLM-L-6-v2`
- `bge-reranker-v2-m3`

## Starting Work

### If Using An AI Coding Assistant

Before asking an assistant to change anything, require it to understand the current project.

The assistant must read:

1. `AGENTS.md`
2. `README.md`
3. `docs/PROJECT_STATUS.md`
4. `docs/ROADMAP.md`
5. `docs/ENGINEERING_WORKFLOW.md`
6. `docs/DEVELOPMENT_ENVIRONMENT.md`
7. `docs/CODING_STANDARDS.md`
8. `docs/AI_AGENT_WORKFLOW.md`
9. `docs/DECISIONS.md`

Rules for AI-assisted work:

- The engineer owns the final change.
- Review every AI-generated edit.
- Keep work inside the assigned Jira ticket.
- Do not allow the assistant to add unrelated features.
- Do not allow paid hosted services or non-local dependencies.
- Run relevant validation commands yourself.
- Update documentation in the same change when behavior, setup, or architecture changes.

### If Not Using An AI Coding Assistant

Read the same project documents manually before implementation:

1. `README.md`
2. `docs/PROJECT_STATUS.md`
3. `docs/ROADMAP.md`
4. `docs/ENGINEERING_WORKFLOW.md`
5. `docs/DEVELOPMENT_ENVIRONMENT.md`
6. `docs/CODING_STANDARDS.md`
7. `docs/DECISIONS.md`

The workflow, review process, documentation expectations, and Definition of Done are identical whether or not AI is used.

## Git Workflow

- `main` is the integration branch.
- Work happens on short-lived branches.
- Use branch names in this format:

```text
feature/<ticket-id>-short-description
```

Examples:

```text
feature/RAG-001-backend-foundation
feature/RAG-014-retrieval-trace-view
```

Every pull request must include:

- Summary of changes.
- Related Jira ticket.
- Implementation notes.
- Testing performed.
- Documentation updates.

At least one engineer must review every pull request before merge.

## Engineering Standards

- Keep changes focused.
- Prefer configuration over hardcoded values.
- Separate business logic from infrastructure concerns.
- Add meaningful logging when implementation exists.
- Handle expected error scenarios.
- Avoid duplicate logic.
- Avoid dead code and commented-out code.
- Do not add temporary workarounds without documenting the reason.
- Keep the implementation aligned with the TDD stage order.

## Documentation Standards

Update documentation whenever implementation changes.

Update `docs/PROJECT_STATUS.md` when project status changes.

Update `docs/DECISIONS.md` when architecture, tooling, model, or workflow decisions change.

Update the relevant area docs when APIs, configuration, deployment, evaluation, or operations behavior changes.

## Day Zero Validation Checklist

Every developer must complete this checklist before feature development.

- [ ] Homebrew installed if using macOS.
- [ ] Git installed and verified.
- [ ] Python 3.11 installed and verified.
- [ ] pip for Python 3.11 installed and verified.
- [ ] Python venv support verified.
- [ ] `uv` installed and verified.
- [ ] Node.js LTS installed and verified.
- [ ] npm installed and verified.
- [ ] pnpm installed and verified.
- [ ] Docker Desktop installed.
- [ ] Docker daemon running.
- [ ] Docker Compose installed and verified.
- [ ] Ollama installed.
- [ ] Ollama server reachable.
- [ ] Required future models identified.
- [ ] No models pulled unless explicitly approved.
- [ ] Repository cloned successfully.
- [ ] Day Zero folder structure confirmed.
- [ ] `.venv` created and verified.
- [ ] No project dependencies installed without approval.
- [ ] `.env.example` reviewed.
- [ ] Project documentation reviewed.
- [ ] Engineering workflow understood.
- [ ] No application feature code created during setup.

If any validation step fails, stop immediately. Create a Jira ticket titled `Day Zero Environment Issue` and include the failed command, output, operating system, and attempted fix.

## Validation Commands

### Git

```bash
git --version
git status --short --branch
```

Expected:

```text
git version 2.40+
## <branch-name>...
```

Common failures:

- `git: command not found`: install Git.
- Authentication failure during clone or push: check SSH keys or HTTPS credentials.

### Python

```bash
python3.11 --version
python3.11 -m pip --version
python3.11 -m venv --help
```

Expected:

```text
Python 3.11.x
pip ... (python 3.11)
usage: venv ...
```

Common failures:

- `python3.11: command not found`: install Python 3.11.
- pip reports another Python version: verify PATH and use `python3.11 -m pip`.

### Virtual Environment

```bash
python3.11 -m venv .venv
.venv/bin/python --version
.venv/bin/python -m pip --version
```

Expected:

```text
Python 3.11.x
pip ... .venv ... (python 3.11)
```

Common failures:

- `.venv` uses the wrong Python: recreate it with `python3.11 -m venv .venv`.
- Permission errors: check repository ownership and filesystem permissions.

### Node And Package Managers

```bash
node --version
npm --version
pnpm --version
```

Expected:

```text
v24.x.x
<npm-version>
<pnpm-version>
```

Common failures:

- Node reports an odd-numbered non-LTS version: install and link Node LTS.
- `pnpm: command not found`: install pnpm.

### Docker

```bash
docker --version
docker compose version
docker context ls
docker --context desktop-linux info
```

Expected:

```text
Docker version ...
Docker Compose version ...
desktop-linux ...
Server: ...
```

Common failures:

- Docker daemon not reachable: open Docker Desktop and wait for startup.
- Permission denied to Docker socket in sandboxed tools: rerun validation from a normal terminal.
- `docker compose` missing: reinstall or repair Docker Desktop CLI plugins.

### Ollama

```bash
ollama --version
ollama list
curl http://localhost:11434/api/tags
```

Expected with no models pulled:

```text
client version is ...
NAME    ID    SIZE    MODIFIED
```

```json
{"models":[]}
```

Common failures:

- `could not connect to ollama server`: run `ollama serve` or `brew services start ollama`.
- Port `11434` unavailable: check whether another process is using the port.
- No models listed: this is expected during Day Zero.

### Repository Structure

```bash
rg --files --hidden -g '!**/.git/**'
find . -maxdepth 3 -type f \( -name 'pyproject.toml' -o -name 'requirements*.txt' -o -name 'package.json' -o -name 'docker-compose.yml' -o -name 'compose.yml' \)
```

Expected:

- Day Zero docs and placeholder folders are present.
- No dependency manifest or Compose file exists until a later approved setup ticket.

Common failures:

- Missing Day Zero docs: pull the latest branch or verify checkout.
- Dependency files unexpectedly present: check whether you are on a later feature branch.

## Definition Of Done For Day Zero

Day Zero is complete when:

- Required machine tools are installed and verified.
- Docker Desktop is running.
- Ollama is reachable.
- The repository is cloned and readable.
- `.venv` exists and uses Python 3.11.
- Project standards docs have been reviewed.
- No feature code has been created.
- No dependencies or models have been installed without approval.
- Any failed validation has been captured in a Jira `Day Zero Environment Issue`.

## Sign-Off

Each engineer should record sign-off in the project tracking system.

```text
Engineer Name:
Date:
Operating System:
Machine:
AI Coding Assistant Used: None / Codex / Claude / GitHub Copilot / Cursor / Windsurf / Other
Validation Status: Pass / Fail
Notes:
```

If validation status is `Fail`, stop immediately and create a `Day Zero Environment Issue` Jira ticket before starting feature development.
