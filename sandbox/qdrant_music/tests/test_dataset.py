from __future__ import annotations

from qdrant_music.dataset import load_dataset, validation_summary
from qdrant_music.settings import SETTINGS


def test_frozen_dataset_is_complete_and_checksummed() -> None:
    summary = validation_summary()

    assert summary["records"] == 50
    assert summary["rank_min"] == 1
    assert summary["rank_max"] == 50
    assert summary["duplicate_ids"] == 0
    assert summary["missing_descriptions"] == 0
    assert summary["sha256"] == SETTINGS.dataset_sha256


def test_stable_point_ids_and_payloads() -> None:
    metadata, songs = load_dataset()
    first = songs[0]

    assert first.point_id == songs[0].point_id
    assert len({song.point_id for song in songs}) == 50
    assert first.payload(metadata)["chart_rank"] == 1
    assert first.payload(metadata)["chart_date"] == "2024-06-01"
    assert isinstance(first.payload(metadata)["community_tags"], list)
