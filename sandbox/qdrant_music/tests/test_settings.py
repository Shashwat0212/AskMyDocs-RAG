from __future__ import annotations

from qdrant_music.settings import SETTINGS


def test_shared_settings_match_tutorial_contract() -> None:
    assert SETTINGS.qdrant_url == "http://localhost:6333"
    assert SETTINGS.qdrant_version == "1.18.2"
    assert SETTINGS.model_name == "nomic-ai/nomic-embed-text-v1.5"
    assert SETTINGS.vector_size == 768
    assert SETTINGS.hnsw_m == 16
    assert SETTINGS.hnsw_ef_construct == 100
    assert SETTINGS.hnsw_full_scan_threshold_kb == 10
    assert SETTINGS.indexing_threshold_kb == 10
    assert "notebook" not in SETTINGS.baseline_collection
    assert "notebook" in SETTINGS.notebook_baseline_collection
