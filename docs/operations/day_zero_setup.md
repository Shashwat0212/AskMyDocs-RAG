# Day Zero Setup Guide

This guide is the onboarding source of truth for AskMyDocs-RAG. It prepares a developer machine and repository checkout before any feature work begins.

It works for developers using Codex, Claude, GitHub Copilot, Cursor, Windsurf, another assistant, or no AI assistant. AI is optional. It is a productivity tool, not a project dependency.

## What Day Zero Does

Day Zero creates a common baseline:

- Required machine tools are installed.
- Docker and Ollama are available locally.
- The repository can be cloned and inspected.
- A Python 3.11 virtual environment can be created.
- Project standards are understood before coding starts.

Day Zero does not build the application. Do not add backend code, frontend code, APIs, retrieval logic, database logic, evaluation logic, caching, deployment pipelines, app dependencies, or model downloads unless a later Jira ticket explicitly approves that work.

## If Your Machine Is Not Suitable

If local setup feels too slow, unstable, or resource-constrained, use a free Google Colab environment for early exploration and learning tasks.

Use Colab only for lightweight experiments, document review, or isolated notebooks. Do not treat Colab as the source of truth for repository state, do not store secrets in notebooks, and do not use it as a replacement for the reviewed local development workflow.

Basic Colab setup:

```python
!git clone <repository-url>
%cd AskMyDocs-RAG
!python --version
!pip --version
```

Colab limitations:

- Docker Desktop is not available.
- Long-running local services such as Qdrant and Ollama may not behave like a developer machine.
- Runtime storage is temporary.
- Any useful code or notes must be moved back into the repository through the normal branch and PR workflow.

## Setup Options

Choose one path:

- Manual setup: follow the commands in this guide.
- Scripted setup on macOS: run `scripts/setup_day_zero_macos.sh`.
- Scripted setup on Windows: run `scripts/setup_day_zero_windows.ps1`.
- AI-assisted setup: ask your assistant to follow this guide exactly, then review every command before running it.

If any step fails, stop. Do not continue to feature work. Create a Jira ticket titled `Day Zero Environment Issue` with the command, output, operating system, and attempted fix.

## Required Tools

| Tool | Required state | Why it is needed | Verify |
|---|---|---|---|
| Git | Installed | Source control | `git --version` |
| Python | 3.11.x | Backend and ML baseline | `python3.11 --version` |
| pip | Python 3.11 pip | Python package tooling | `python3.11 -m pip --version` |
| venv | Python 3.11 venv | Local virtual environment | `python3.11 -m venv --help` |
| uv | Installed | Preferred Python environment/package tool | `uv --version` |
| Node.js | Active LTS, Node 24 currently | Future frontend work | `node --version` |
| npm | Installed | Node package tooling | `npm --version` |
| pnpm | Installed | Preferred frontend package manager | `pnpm --version` |
| Docker Desktop | Installed and running | Local containers, future Qdrant | `docker --version` |
| Docker Compose | Installed | Local service orchestration | `docker compose version` |
| Ollama | Installed and reachable | Local model serving | `ollama list` |
| curl | Installed | HTTP validation | `curl --version` |
| wget | Installed | Download utility | `wget --version` |
| make | Installed | Common command runner | `make --version` |
| jq | Installed | JSON inspection | `jq --version` |
| unzip | Installed | Archive handling | `unzip -v` |

## Scripted Setup

The setup scripts install and verify machine tools only. They do not install project app dependencies, create application code, pull models, or create deployment files.

### macOS

From the repository root:

```bash
chmod +x scripts/setup_day_zero_macos.sh
./scripts/setup_day_zero_macos.sh
```

What it does:

- Verifies or installs Homebrew.
- Installs missing tools with Homebrew.
- Installs Python 3.11, uv, Node 24 LTS, pnpm, Docker Desktop, Ollama, wget, jq, and supporting tools.
- Creates `.venv` if it does not exist.
- Verifies Docker Desktop and Ollama.
- Stops immediately on failure and prints the next action.

### Windows

Run PowerShell as your normal user. Administrator mode may be required for Docker Desktop or winget-managed installs.

From the repository root:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\setup_day_zero_windows.ps1
```

What it does:

- Verifies `winget`.
- Installs missing tools through `winget`, official installers, or built-in Windows capabilities.
- Enables Corepack and pnpm.
- Creates `.venv` if it does not exist.
- Verifies Docker Desktop and Ollama.
- Stops immediately on failure and prints the next action.

After scripted setup, rerun the validation section manually. The engineer owns the final sign-off even when a script or assistant performed the setup.

## Manual Setup: macOS

Install missing tools only:

```bash
brew install python@3.11
brew install uv
brew install node@24
brew unlink node
brew link node@24 --force --overwrite
brew install pnpm
brew install --cask docker
brew install ollama
brew install wget jq
```

Open Docker Desktop:

```bash
open -a Docker
```

Start Ollama if it is not already running:

```bash
ollama serve
```

or:

```bash
brew services start ollama
```

Do not pull models during Day Zero unless explicitly approved.

## Manual Setup: Windows

Install missing tools with `winget`:

```powershell
winget install --id Git.Git -e
winget install --id Python.Python.3.11 -e
winget install --id OpenJS.NodeJS.LTS -e
winget install --id Docker.DockerDesktop -e
winget install --id Ollama.Ollama -e
winget install --id jqlang.jq -e
winget install --id JernejSimoncic.Wget -e
winget install --id GnuWin32.Make -e
```

Install uv:

```powershell
powershell -ExecutionPolicy Bypass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Enable pnpm:

```powershell
corepack enable
corepack prepare pnpm@latest --activate
```

Windows includes `curl` and archive tooling by default. The setup script still checks `wget`, `make`, and archive support so the command set stays consistent across the team.

Open Docker Desktop from the Start menu and wait for it to finish startup.

Start Ollama from the Start menu, or run:

```powershell
ollama serve
```

Do not pull models during Day Zero unless explicitly approved.

## Repository Setup

Clone and enter the repository:

```bash
git clone <repository-url>
cd AskMyDocs-RAG
```

Check the branch and files:

```bash
git status --short --branch
rg --files --hidden -g '!**/.git/**'
```

Expected Day Zero folders:

```text
AGENTS.md
CLAUDE.md
CODEX.md
KNOWLEDGE.md
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

Create the virtual environment if it does not exist:

macOS/Linux:

```bash
python3.11 -m venv .venv
.venv/bin/python --version
.venv/bin/python -m pip --version
```

Windows PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip --version
```

Do not install project dependencies yet. At Day Zero the repository intentionally has no `pyproject.toml`, `requirements.txt`, `package.json`, lockfiles, or Docker Compose file.

## Environment Configuration

Use `.env.example` as the reference for variable names. Do not commit `.env`.

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

The files in `configs/` are examples only. Do not create runtime config files such as `configs/models.yaml` unless a setup ticket approves that step.

## Local Services

Day Zero validates only the local tooling.

Ollama should be reachable:

```bash
ollama list
curl http://localhost:11434/api/tags
```

Expected output when no models are installed:

```text
NAME    ID    SIZE    MODIFIED
```

```json
{"models":[]}
```

Qdrant is not validated yet because this repository intentionally has no Docker Compose file. Qdrant setup belongs in a later approved setup ticket.

Required future models are identified but not pulled:

- `qwen3:4b`
- `qwen2.5:7b-instruct`
- `deepseek-r1-distill-qwen:7b`
- `nomic-embed-text-v1.5`
- `bge-small-en-v1.5`
- `cross-encoder/ms-marco-MiniLM-L-6-v2`
- `bge-reranker-v2-m3`

## Starting Work

### With An AI Coding Assistant

Before any edit, the assistant must read:

1. `starter.md`
2. `AGENTS.md`

Then use the task-routing table in `starter.md` to read the detailed sources required for the task. Architecture, roadmap, stack, constraint, and stage-order changes also require both governing DOCX files.

Rules:

- The engineer owns the final change.
- Review every AI-generated edit.
- Keep work inside the assigned Jira ticket.
- Do not allow unrelated features.
- Do not introduce paid hosted services.
- Run validation yourself.
- Update documentation when behavior, setup, or architecture changes.
- Update affected folder-level `KNOWLEDGE.md` files when code, configuration, scripts, documentation structure, or behavior changes.

### Without An AI Coding Assistant

Read the same project documents manually before implementation. The workflow, review process, documentation expectations, and Definition of Done are identical whether AI is used or not.

## Git Workflow

- `main` is the integration branch and implementation baseline.
- `project-governance` is the permanent planning and project-state branch.
- Implementation work happens on short-lived feature branches created from `main`.
- Branch names use:

```text
feature/<ticket-id>-short-description
```

Every pull request includes:

- Summary of changes.
- Related Jira ticket.
- Implementation notes.
- Testing performed.
- Documentation updates.

At least one engineer reviews every pull request before merge.

## Validation Checklist

Complete this before feature development:

- [ ] Git installed and verified.
- [ ] Python 3.11 installed and verified.
- [ ] Python 3.11 pip and venv verified.
- [ ] `uv` installed and verified.
- [ ] Node.js LTS, npm, and pnpm verified.
- [ ] Docker Desktop installed and running.
- [ ] Docker Compose verified.
- [ ] Ollama installed and reachable.
- [ ] Required future models identified.
- [ ] No models pulled unless approved.
- [ ] Repository cloned successfully.
- [ ] Day Zero folder structure confirmed.
- [ ] `.venv` created and verified.
- [ ] No project dependencies installed without approval.
- [ ] `.env.example` reviewed.
- [ ] Project documentation reviewed.
- [ ] Root and folder-level knowledge documentation reviewed.
- [ ] Engineering workflow understood.
- [ ] No application feature code created during setup.

If any item fails, stop and create a `Day Zero Environment Issue` Jira ticket.

## Validation Commands

### Git

```bash
git --version
git status --short --branch
```

Expected: Git version prints and the current branch is shown.

If it fails: install Git, fix repository permissions, or repair credentials.

### Python And Virtual Environment

macOS/Linux:

```bash
python3.11 --version
python3.11 -m pip --version
python3.11 -m venv --help
test -d .venv || python3.11 -m venv .venv
.venv/bin/python --version
```

Windows PowerShell:

```powershell
py -3.11 --version
py -3.11 -m pip --version
py -3.11 -m venv --help
if (-not (Test-Path .venv)) { py -3.11 -m venv .venv }
.\.venv\Scripts\python.exe --version
```

Expected: Python reports 3.11.x and the venv Python also reports 3.11.x.

If it fails: install Python 3.11 and recreate `.venv`.

### Node

```bash
node --version
npm --version
pnpm --version
```

Expected: Node reports an LTS version, currently `v24.x.x`.

If it fails: install Node LTS and pnpm, then reopen the terminal.

### Docker

```bash
docker --version
docker compose version
docker context ls
docker --context desktop-linux info
```

Expected: Docker and Compose versions print; Docker Desktop server info is available.

If it fails: open Docker Desktop, wait for startup, and retry. If socket access fails from an AI tool sandbox, retry from a normal terminal.

### Ollama

```bash
ollama --version
ollama list
curl http://localhost:11434/api/tags
```

Expected with no models:

```text
NAME    ID    SIZE    MODIFIED
```

```json
{"models":[]}
```

If it fails: start Ollama with `ollama serve` or the desktop app, then retry.

### Repository Shape

```bash
rg --files --hidden -g '!**/.git/**'
find . -maxdepth 3 -type f \( -name 'pyproject.toml' -o -name 'requirements*.txt' -o -name 'package.json' -o -name 'docker-compose.yml' -o -name 'compose.yml' \)
```

Expected: Day Zero files exist; no app dependency or Compose manifests exist yet.

If it fails: pull the latest branch or confirm you are on the intended feature branch.

## Day Zero Sign-Off

Record sign-off in Jira or the project tracker:

```text
Engineer Name:
Date:
Operating System:
Machine:
AI Coding Assistant Used: None / Codex / Claude / GitHub Copilot / Cursor / Windsurf / Other
Validation Status: Pass / Fail
Notes:
```

If validation is `Fail`, do not start feature development. Create a `Day Zero Environment Issue` Jira ticket first.
