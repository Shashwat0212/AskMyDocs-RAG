# Deployment Knowledge

## Current State

The deployment folder contains `compose.qdrant.yaml`, the pinned, loopback-only
Qdrant 1.18.2 service approved for the RAG-002 learning sandbox. It uses a named
volume so normal shutdown preserves collections.

## Planned Responsibility

This folder owns approved local service orchestration assets. The current
Compose file is an educational single-node service, not a production
deployment. Cloudflare Tunnel and GitHub Pages remain future-stage work.

## Update Notes

Update this file when deployment assets or operational deployment instructions are added. Do not introduce deployment pipelines before the approved deployment stage.
