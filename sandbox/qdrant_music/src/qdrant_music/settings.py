"""Shared, configuration-first settings for every RAG-002 learning path."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _repository_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "starter.md").exists() and (parent / "AGENTS.md").exists():
            return parent
    raise RuntimeError("Could not locate the AskMyDocs repository root")


@dataclass(frozen=True)
class SandboxSettings:
    repository_root: Path
    qdrant_url: str
    qdrant_version: str
    model_name: str
    vector_size: int
    baseline_collection: str
    hnsw_collection: str
    notebook_baseline_collection: str
    notebook_hnsw_collection: str
    hnsw_m: int
    hnsw_ef_construct: int
    hnsw_full_scan_threshold_kb: int
    indexing_threshold_kb: int
    dataset_path: Path
    dataset_sha256: str


_ROOT = _repository_root()

SETTINGS = SandboxSettings(
    repository_root=_ROOT,
    qdrant_url=os.getenv("QDRANT_URL", "http://localhost:6333"),
    qdrant_version="1.18.2",
    model_name=os.getenv(
        "QDRANT_TUTORIAL_EMBEDDING_MODEL",
        "nomic-ai/nomic-embed-text-v1.5",
    ),
    vector_size=768,
    baseline_collection=os.getenv(
        "QDRANT_TUTORIAL_BASELINE_COLLECTION",
        "billboard_top50_baseline",
    ),
    hnsw_collection=os.getenv(
        "QDRANT_TUTORIAL_HNSW_COLLECTION",
        "billboard_top50_hnsw_lab",
    ),
    notebook_baseline_collection="billboard_top50_notebook_baseline",
    notebook_hnsw_collection="billboard_top50_notebook_hnsw",
    hnsw_m=16,
    hnsw_ef_construct=100,
    hnsw_full_scan_threshold_kb=10,
    indexing_threshold_kb=10,
    dataset_path=(
        _ROOT
        / "sandbox"
        / "qdrant_music"
        / "fixtures"
        / "billboard_hot_100_2024-06-01_top50.json"
    ),
    dataset_sha256="2270a686e00379eaff8bac28c1822554ec3db1eb49330b54787f7eaca37d7ed5",
)

PHASE_IDS = tuple(f"Q{index:02d}" for index in range(17))
DEFAULT_QUERY = "uplifting energetic pop with a strong dance feel"
