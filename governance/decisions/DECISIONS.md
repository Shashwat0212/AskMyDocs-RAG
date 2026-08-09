# Decision Log

Record important architecture, tooling, model, workflow, and repository decisions here.

## Format

```text
Date: YYYY-MM-DD
Status: Active | Superseded
Decision:
Rationale:
Consequences:
Supersedes: Optional date or decision reference
```

Entries without an explicit status are active. Superseded entries remain in the log to preserve decision history.

## Decisions

Date: 2026-07-02
Decision: Establish Day Zero foundation before feature development.
Rationale: The team will use multiple AI coding assistants and needs shared standards, status tracking, and repository structure before implementation begins.
Consequences: The repository starts with documentation, configuration examples, and placeholder folders only. Application features begin after a reviewed feature ticket.

Date: 2026-07-02
Decision: Use `AGENTS.md` as the canonical AI-agent instruction file.
Rationale: Codex, Claude, GitHub Copilot, and future tools need a shared source of project rules.
Consequences: Assistant-specific files should stay thin and point back to `AGENTS.md`.

Date: 2026-07-03
Status: Superseded by the 2026-08-04 Qdrant-native Phase 1 retrieval decision.
Decision: Scope Phase 1 to staged Core RAG MVP epics with lightweight hybrid retrieval.
Rationale: The project owner wants the MVP retrieval plan to include hybrid retrieval without pulling in Stage 2 reranking, inspection, or quality-mode complexity.
Consequences: Phase 1 will target dense vector retrieval plus a simple local lexical path with configurable fusion. Retrieval inspection UI, quality model mode, evaluation automation, caching, routing, arbitration, and the final React/Next.js interface remain outside Phase 1. The later 2026-07-05 decision merges the first two setup epics while preserving this scope boundary. The later 2026-07-07 decision adds reranking and session memory as post-MVP Phase 1 enhancement epics, after the lean MVP UI is working.

Date: 2026-07-03
Status: Superseded by the 2026-08-09 governance-only branch structure decision.
Decision: Store the owner-provided Technical Design Document and Approach document in the repository under `docs/source_documents/`.
Rationale: The project rules treat these documents as the governing source of truth, so agents and contributors need stable repo-local paths.
Consequences: Future roadmap, architecture, workflow, and implementation changes must be checked against the DOCX source documents before proceeding.

Date: 2026-07-05
Decision: Establish `KNOWLEDGE.md` as the folder-level knowledge documentation convention.
Rationale: The project needs durable, local-first knowledge sharing so contributors and AI agents can understand what each folder currently contains and what related documentation must change with implementation work.
Consequences: Every project-owned folder should contain a `KNOWLEDGE.md` file. The repository root `KNOWLEDGE.md` maps child knowledge docs. Changes to code, configuration, scripts, documentation structure, or behavior must update affected folder-level knowledge docs in the same change, and folder structure changes must update the root map.

Date: 2026-07-05
Status: Superseded by the 2026-07-27 final Epic 1 ticket consolidation decision.
Decision: Merge the Phase 1 backend foundation and local service infrastructure epics into a single Backend Foundations And Local Tooling Familiarization epic.
Rationale: The project owner wants the first Phase 1 work to combine developer familiarization, FastAPI backend setup, local Qdrant validation, local Ollama validation, and repeatable operations commands before product feature development begins.
Consequences: The first Phase 1 epic now covers tickets `RAG-001` through `RAG-006`. It remains setup-focused and documentation-driven where appropriate. Document upload, ingestion, embeddings, retrieval, answer generation, Gradio UI, deployment pipelines, and feature integrations remain outside this merged setup epic.

Date: 2026-07-07
Status: Superseded by the 2026-08-04 seven-epic Phase 1 sequence decision.
Decision: Add reranking and session memory as separate post-MVP Phase 1 enhancement epics.
Rationale: The first MVP should stay lean and prove document-grounded upload, indexing, retrieval, answer generation, and Gradio UI before adding another retrieval-quality model or conversation-memory layer.
Consequences: Epics 1 through 6 deliver the first MVP. Epic 7 adds optional local reranking, disabled by default and starting with a local cross-encoder approach rather than LLM reranking. Epic 8 adds session memory and conversation retrieval with local SQLite-backed chat storage and separate memory indexes. Hosted or paid reranking, memory, and observability services remain prohibited.

Date: 2026-07-07
Decision: Use flow-level tracing and local-first open-source observability for backend measurement.
Rationale: The project needs one trace identifier per user workflow plus measurable spans and metrics for future SLA/SLO tracking without building a custom observability framework or using paid hosted services.
Consequences: Backend observability should use one workflow `trace_id`, trace-aware logs, OpenTelemetry-compatible spans, Prometheus-compatible metrics, and self-hosted Grafana OSS dashboards when implemented. VizTracer remains optional local developer profiling. Hosted tracing, Grafana Cloud, managed Prometheus, and paid observability platforms remain prohibited.

Date: 2026-07-07
Decision: Treat chunking and retrieval behavior as configurable strategy-based hyperparameters.
Rationale: Chunking, retrieval mode, lexical strategy, fusion strategy, and related parameters materially affect RAG quality and need to be tuned without rewriting ingestion or retrieval code.
Consequences: Chunking should use a pluggable strategy interface selected by configuration. Retrieval should expose configurable dense, lexical, and fusion behavior. Future strategy additions should be isolated modules behind stable interfaces.

Date: 2026-07-07
Status: Superseded by the 2026-08-04 Qdrant-native Phase 1 retrieval decision.
Decision: Use a canonical local chunk store with Qdrant and lexical search as separate indexes.
Rationale: Full chunk text should not be duplicated by default across Qdrant payloads and lexical indexes. A local canonical chunk store keeps source text and metadata in one place while Qdrant and BM25/FTS indexes reference chunks by ID.
Consequences: Phase 1 indexing should prefer SQLite or equivalent local storage for canonical chunk records, Qdrant for dense vector indexing with lightweight payloads, and SQLite FTS5/BM25 or equivalent local lexical indexing over the same chunk IDs. Retrieval hydrates final results from the canonical chunk store.

Date: 2026-07-08
Status: Superseded by the 2026-08-04 seven-epic Phase 1 sequence and experiment-prototype decisions.
Decision: Add a post-MVP hyperparameter experimentation and blueprinting epic.
Rationale: The project owner wants a local module that can use configuration as a control plane, run permutations of implemented RAG hyperparameters over evaluation datasets, compare results, and build practical guidance for different document qualities, industries, and use cases.
Consequences: Phase 1 now includes Epic 9 after reranking and session memory. The experimentation module should stay local-first, configuration-driven, and offline by default. It can vary only implemented pipeline options and should record run manifests, metrics, latency, errors, and artifacts. Paid hosted experiment tracking and automatic production tuning remain prohibited.

Date: 2026-07-13
Status: Superseded by the 2026-07-14 permanent governance branch decision.
Decision: Keep project tracking and decision documents on `main` and update them through short-lived ticket branches.
Rationale: Jira should own ticket execution while the repository keeps durable status, plans, and decisions beside the code they govern. A permanent tracking branch would drift from implementation and create a competing project state.
Consequences: `docs/PROJECT_TRACKING.md` defines synchronization rules. `docs/PROJECT_STATUS.md` keeps the current project and Epic 1 snapshot. Future ticket branches must update status, plans, decisions, and knowledge docs when their changes affect project state, then merge those updates into `main`.

Date: 2026-07-14
Status: Superseded by the 2026-08-09 standalone governance and selective-promotion decision.
Decision: Maintain `project-governance` as the permanent planning and project-state branch with two-way synchronization to `main`.
Rationale: The project owner uses Codex to inspect future epics, evolve possible directions, and keep those prospects visible without treating every exploration as an approved implementation decision. A permanent branch provides that working space while approved checkpoints on `main` keep implementation agents aligned.
Consequences: `project-governance` holds the latest project snapshot, future prospects, and proposed planning changes. Approved governance pull requests use merge commits into `main`, and completed implementation changes are merged back into `project-governance`. Jira synchronization remains manual, and application code must not be implemented on the governance branch. The later 2026-07-18 decision defines the implementation branch hierarchy.
Supersedes: The 2026-07-13 decision requiring all governance work to use short-lived branches.

Date: 2026-07-14
Status: Superseded by the 2026-08-09 governance-only branch structure decision.
Decision: Use root `starter.md` as the mandatory primary briefing for every new work session.
Rationale: Contributors and AI agents need a fast, reliable orientation to current project state and next work without rereading the complete repository on every run.
Consequences: Every run begins with `starter.md` and `AGENTS.md`, followed by task-specific sources selected through the starter's routing table. The starter remains a summary rather than a competing source of truth. Both governing DOCX files remain mandatory before changing architecture, roadmap direction, selected stack, project constraints, or stage ordering.

Date: 2026-07-18
Status: Active
Decision: Use short-lived epic integration branches with developer-namespaced ticket branches.
Rationale: Epic-level integration provides a review boundary for validating related setup work together, while developer namespaces make concurrent ticket ownership visible and avoid branch-name collisions.
Consequences: Epic branches start from the approved `main` baseline and use `epic/<epic-id>-short-description`. Ticket branches start from the latest active epic branch, use `feature/<developer>/<ticket-id>-short-description`, and target the epic branch in pull requests. A validated epic branch targets `main`. Ticket and epic branches are deleted after their respective merges; `project-governance` remains permanent and contains no application code. Epic 1 uses `epic/epic-1-backend-foundations`, and Shashwat's first ticket uses `feature/shashwat/RAG-001-fastapi-sandbox`.

Date: 2026-07-27
Status: Active
Decision: Use a final four-ticket structure for Epic 1.
Rationale: The project owner explicitly merged the FastAPI learning, backend skeleton, settings, logging, and test work into one tutorial ticket while retaining separate Qdrant, Ollama, and operations tickets.
Consequences: Epic 1 contains `RAG-001` plus three Jira-key-pending tickets: Docker Compose and Qdrant sandbox, Ollama sandbox, and local commands and operations. The six detailed learning steps remain useful, but they do not represent six separate Jira tickets. Product ingestion, retrieval, generation, and UI features remain outside Epic 1.
Supersedes: The six-ticket enumeration in the 2026-07-05 merged Epic 1 decision.

Date: 2026-08-04
Status: Active
Decision: Use a phase-specific execution model: Epic 1 local, Epics 2 through 6 on free-tier Google Colab, and Epic 7 on the local MVP runtime.
Rationale: Free-tier Colab gives contributors a common development environment and equal access to compute, while the product must still prove that the selected configuration runs locally for the MVP.
Consequences: Free Colab is the explicit hosted-compute exception. Qdrant and Ollama remain pinned, self-managed processes inside the runtime. Colab Qdrant data stays on the runtime filesystem and is disposable. Git stores reviewed code, compact configuration, manifests, selected profiles, fixtures, and summaries; the configured shared Drive stores datasets and full run artifacts. Experiment automation is manually launched, end-to-end automated, checkpointed, resumable, and failure-isolated rather than unattended scheduling. Paid APIs, paid inference, hosted vector databases, paid evaluation, paid observability, and paid experiment tracking remain prohibited.
Supersedes: Active claims that Phase 1 development is local-only or that Colab is reserved for incidental experiments.

Date: 2026-08-04
Status: Active
Decision: Use self-managed Qdrant as the only Phase 1 document indexing and retrieval engine.
Rationale: Qdrant supports named dense and sparse vectors, BM25/sparse retrieval, filters, complete payloads, and native hybrid Query API fusion in one rebuildable boundary.
Consequences: Phase 1 stores full retrievable chunk text and citation metadata in Qdrant payloads, uses named dense and sparse/BM25 vectors, starts with RRF fusion, and keeps DBSF configurable. Source documents and dataset manifests are the durable canonical records from which ephemeral collections are rebuilt. SQLite is removed from the Phase 1 document chunk, lexical-search, hydration, and retrieval path; this decision does not prohibit a separately approved future local database for unrelated concerns such as session memory.
Supersedes: The 2026-07-03 lightweight split-retrieval decision and the 2026-07-07 canonical local chunk store decision.

Date: 2026-08-04
Status: Superseded by the 2026-08-09 retrieval-first Phase 1 sequence decision.
Decision: End Phase 1 at seven epics, with reranking in Epic 4, experimentation and the configuration navigator in Epic 5, generation in Epic 6, and the local Gradio MVP in Epic 7.
Rationale: Retrieval and reranking must be measured and configured before LLM integration, and the former Epic 9 experiment work is now a required selection gate rather than a post-MVP enhancement.
Consequences: Epic 1 remains the unchanged four-ticket local foundation. Epics 2 through 6 run canonically in Colab. The lean MVP boundary moves to Epic 7. Session memory moves outside Phase 1 and receives no Phase 1 epic number. Ticket references are renumbered sequentially from `RAG-001` through `RAG-041`; any reference not yet created in Jira is provisional.
Supersedes: The 2026-07-07 reranking/session-memory epic decision and the 2026-07-08 Epic 9 experimentation decision.

Date: 2026-08-04
Status: Superseded by the 2026-08-09 benchmark-trained navigator decision.
Decision: Use three versioned configuration contracts and a two-level configuration navigator.
Rationale: Index-time decisions cannot safely be changed at query time, and every selected setting must be reproducible across disposable Colab sessions and the local MVP runtime.
Consequences: An ingestion/index profile owns parser, chunking, embedding, dimensions, collection/index settings, and payload schema. A query profile owns compatible candidate limits, filters, fusion, thresholds, reranking, and final count. A run manifest records source commit, dataset/checksum, runtime details, profile/config hash, Qdrant/model versions, metrics, errors, state, and artifact locations. The pre-ingestion scanner selects one index profile or a configured resource-capped alternative set when uncertain; the query-time navigator changes only settings compatible with existing collections and reports selection provenance.

Date: 2026-08-04
Status: Superseded by the 2026-08-09 retrieval evaluation and profile experiment decisions.
Decision: Implement Epic 5 experimentation from an isolated branch snapshot, then merge validated architecture back and remove the temporary copy.
Rationale: Experiments need freedom to compare plug-in strategies without creating a permanent divergent product implementation.
Consequences: The completed Epic 4 integration commit is recorded in every run manifest. Epic 5 compares granular multi-dataset configurations and reports per-dataset/profile winners and Pareto trade-offs, not a universal winner. Validated interfaces, profiles, and navigator contracts merge into the product pipeline before the epic closes, and the temporary copied prototype is removed. Full LLM, prompt, and generation evaluation remains outside Epic 5; TurboQuant remains exploratory until compatibility is proven.

Date: 2026-08-09
Status: Active
Decision: Make `project-governance` a standalone documentation-only branch and promote approved plans selectively.
Rationale: The project owner wants governance to remain easy to read without carrying the application scaffold or making branch-wide merges that can delete or overwrite implementation files.
Consequences: The branch contains `START_HERE.md`, agent guidance, and a single `governance/` hierarchy for status, roadmap, epics, decisions, standards, handoffs, sources, and references. It is never merged wholesale with `main` in either direction. Approved work moves through a focused handoff that records the governance commit, target epic/tickets, branch, scope, and acceptance criteria. Implementation results are recorded back by commit reference. The `KNOWLEDGE.md` convention remains active on implementation branches but is not used in this documentation-only branch. The original source DOCX files move unchanged to `governance/sources/`.
Supersedes: The 2026-07-14 two-way synchronization decision, the root `starter.md` naming decision for this branch, and the 2026-07-03 source-document path decision.

Date: 2026-08-09
Status: Active
Decision: Use a retrieval-first seven-epic Phase 1 sequence ending at `RAG-047`.
Rationale: Indexing and retrieval form one engineering flow, retrieval needs a formal benchmark before configuration experiments, and profile selection must be validated before answer generation and the final UI.
Consequences: The previous indexing and retrieval epics merge into Epic 3 (`RAG-011`–`RAG-021`). Epic 4 (`RAG-022`–`RAG-028`) builds the retrieval benchmark. Epic 5 (`RAG-029`–`RAG-037`) creates profiles and navigators. Generation remains Epic 6 (`RAG-038`–`RAG-041`), and the local Gradio MVP remains Epic 7 (`RAG-042`–`RAG-047`). Ticket IDs not confirmed in Jira remain provisional. Epics 2–6 continue to use free-tier Colab, and Epics 1 and 7 remain local.
Supersedes: The 2026-08-04 Phase 1 ticket sequence through `RAG-041`.

Date: 2026-08-09
Status: Active
Decision: Build a scale-aware, human-approved retrieval benchmark before profile experiments.
Rationale: Retrieval settings should be judged on whether they find approved source evidence as corpus size and distractor content change, independently of the generation model and available inference budget.
Consequences: Epic 4 uses financial/regulatory, technical/manual, and policy/procedural corpora at approximately 10 thousand, 1 million, and 100 million extracted tokens. Five deterministic distractor variants per family and size create 45 corpus instances. Codex drafts 300 questions and their evidence, but a human must approve every scored record. Canonical labels use stable source spans rather than chunk IDs. The benchmark keeps 210 development questions and 90 source-separated locked-holdout questions. Deterministic Recall, Precision, nDCG, MRR, complete evidence coverage, and latency metrics compare dense-only, sparse-only, hybrid, and hybrid-plus-reranker baselines.

Date: 2026-08-09
Status: Active
Decision: Select versioned profiles with bounded experiments and use explainable decision trees for navigation.
Rationale: Corpus-scale and query characteristics can favor different settings, but unrestricted configuration grids and opaque model-based routing would be expensive and difficult to explain.
Consequences: Epic 5 screens one configuration family at a time, combines only promising candidates, and runs the 100-million-token tier only for baselines and shortlisted candidates. An ingestion tree selects settings that require collection creation; a query tree selects only collection-compatible retrieval settings. The ingestion tree has maximum depth 3 and at least four observations per leaf. The query tree has maximum depth 5 and at least ten queries per leaf. Both use grouped validation, return confidence and reason paths, and use a reviewed `safe-default` when confidence is below 0.70, features are missing or out of range, or compatibility fails. Corpus-family names are not tree inputs.
Supersedes: The 2026-08-04 navigator fallback and experiment-prototype decisions.

Date: 2026-08-09
Status: Active
Decision: Make retrieval the primary Phase 1 quality claim and keep broad generation evaluation outside Phase 1.
Rationale: Retrieval configuration is engineered by this project, while answer coherence depends strongly on the replaceable generation model and available hardware budget.
Consequences: Epic 6 tests bounded context assembly, citations, abstention, trace/profile provenance, timeouts, runtime failures, and smoke behavior. It does not rank LLMs or use model-dependent answer quality to judge retrieval. Ragas, DeepEval, LLM-as-judge scoring, and broad answer-quality comparison remain in the later Generation and System Evaluation stage.
