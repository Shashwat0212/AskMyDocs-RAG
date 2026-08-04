# Configuration Knowledge

## Current Contents

This folder contains examples for model serving, dense/sparse embeddings, Qdrant-native hybrid retrieval, reranking, prompts, and evaluation. `retrieval.example.yaml` illustrates the ingestion/index profile, query profile, navigator boundary, and run-manifest requirements; `models.example.yaml` illustrates self-managed model adapters.

## Responsibilities

Configuration keeps parser/chunking, embedding dimensions, Qdrant schema/index settings, dense/sparse candidate limits, filters, fusion, thresholds, reranking, model names, and artifact locations out of business logic. Epic 5 validates final profiles and navigator parameters through reproducible evidence.

## Persistence And Safety

Reviewed profiles, manifests, and compact summaries may be committed. Datasets and full experiment artifacts belong in configured shared Drive storage. Qdrant live storage stays on the Colab runtime filesystem during Epics 2–6. Do not store secrets, credentials, or machine-specific paths in committed runtime files.

## Update Notes

Update this file when examples, schemas, runtime meaning, or the Git/Drive/runtime boundary changes.
