# Epic 1 Jira Reference

Last reviewed: 2026-07-18

Status: Working reference for manual Jira entry. This file does not record approved Jira state or change project governance.

> Branch-policy warning: the wording below describes the owner's proposed epic-branch workflow. Current governing documentation still requires implementation branches to start from `main` and merge into `main`. Do not use the proposed workflow until the governing policy is formally updated.

Jira will assign the actual issue keys. Replace `<JIRA-KEY>` and `<EPIC-BRANCH>` when the work items and epic branch exist.

## Epic 1: Backend Foundations And Local Tooling Familiarization

### Description

Learn FastAPI, create a backend sandbox, and verify Qdrant, Ollama, and repeatable local development commands.

### Objective

Provide a working local foundation developers can understand, test, operate, and extend during later RAG epics.

### Task Details

- Create `<EPIC-BRANCH>` from the approved implementation baseline.
- Create each ticket branch from the latest epic branch.
- Name ticket branches `feature/<JIRA-KEY>-short-description`.
- Merge ticket pull requests into the epic branch.
- Merge the validated epic branch into `main`.

### Acceptance Criteria

- FastAPI sandbox runs locally.
- Qdrant and Ollama are independently verified.
- Common development commands are documented.
- All ticket changes are reviewed and integrated.
- No document-ingestion or RAG features are implemented.

## Ticket: FastAPI Tutorial And Backend Sandbox

### Description

Follow a FastAPI tutorial, build a small backend skeleton, and experiment with basic settings and logging.

### Objective

Understand FastAPI fundamentals and leave a simple, runnable backend foundation for later tickets.

### Task Details

- Create `feature/<JIRA-KEY>-fastapi-sandbox` from `<EPIC-BRANCH>`.
- Follow a suitable FastAPI tutorial.
- Add a minimal application and health endpoint.
- Experiment with routing, settings, logging, and tests.
- Document useful commands and findings.
- Target `<EPIC-BRANCH>` in the pull request.
- Reference: [FastAPI official tutorial](https://fastapi.tiangolo.com/tutorial/).

### Acceptance Criteria

- FastAPI starts locally.
- Health endpoint returns HTTP 200.
- Interactive API documentation loads.
- Basic settings and logging are demonstrated.
- At least one health-endpoint test passes.
- No RAG features are implemented.

## Ticket: Docker Compose And Qdrant Local Sandbox

### Description

Run Qdrant locally and practice collection creation, vector upsert, search, deletion, and service operations.

### Objective

Confirm developers can independently start, inspect, use, stop, and troubleshoot the local Qdrant service.

### Task Details

- Create `feature/<JIRA-KEY>-qdrant-sandbox` from `<EPIC-BRANCH>`.
- Add a minimal Compose service using a pinned image.
- Configure local persistence and readiness checking.
- Test collection creation, upsert, search, and deletion.
- Document start, stop, logs, health, and reset commands.
- Target `<EPIC-BRANCH>` in the pull request.
- Video: [Qdrant 101: Getting Started](https://youtu.be/LRcZ9pbGnno).
- Reference: [Qdrant local quickstart](https://qdrant.tech/documentation/quick-start/).

### Acceptance Criteria

- Compose configuration is valid.
- Qdrant starts and becomes ready.
- Basic collection operations succeed.
- Normal shutdown preserves stored data.
- Destructive reset is clearly identified.
- No backend Qdrant integration is added.

## Ticket: Ollama Local Model Sandbox

### Description

Verify Ollama locally and test a small generation request through both the CLI and HTTP API.

### Objective

Confirm local model serving works before Ollama integration begins during the answer-generation epic.

### Task Details

- Create `feature/<JIRA-KEY>-ollama-sandbox` from `<EPIC-BRANCH>`.
- Verify the Ollama installation and service.
- Pull or use an approved local model.
- Test CLI and local HTTP generation.
- Document setup, verification, and common failures.
- Target `<EPIC-BRANCH>` in the pull request.
- Video: [Exploring Ollama's REST API](https://youtu.be/PTJAflNXeio).
- Reference: [Ollama quickstart](https://docs.ollama.com/quickstart).

### Acceptance Criteria

- Ollama version and local service are verified.
- An approved local model is available.
- CLI and HTTP generation succeed.
- No backend Ollama client is added.
- No models or generated responses are committed.
- Setup and verification are documented.

## Ticket: Local Backend Commands And Operations

### Description

Create a clear workflow for running, testing, checking, and stopping the backend and local services.

### Objective

Let contributors operate the Epic 1 environment without searching across multiple documents.

### Task Details

- Create `feature/<JIRA-KEY>-local-operations` from `<EPIC-BRANCH>`.
- Document backend setup, start, and test commands.
- Document Qdrant start, stop, health, logs, and reset commands.
- Document Ollama availability and model-list commands.
- Add simple shortcuts where useful.
- Clearly label destructive commands.
- Target `<EPIC-BRANCH>` in the pull request.
- Video: [Docker Compose Tutorial for Beginners](https://youtu.be/MVIcrmeV_6c).
- Reference: [Docker Compose quickstart](https://docs.docker.com/compose/gettingstarted/).

### Acceptance Criteria

- Backend start and test commands work.
- Qdrant operational commands work.
- Ollama verification commands work.
- Destructive commands include clear warnings.
- Missing prerequisites produce understandable errors.
- Documentation is concise and discoverable.
