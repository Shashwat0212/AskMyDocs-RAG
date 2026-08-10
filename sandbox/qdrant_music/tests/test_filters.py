from __future__ import annotations

from qdrant_client import models

from qdrant_music.qdrant_ops import build_filter


def test_empty_filter_returns_none() -> None:
    assert build_filter() is None


def test_filter_contains_requested_conditions() -> None:
    result = build_filter(
        required_tag="dance-pop",
        max_chart_rank=40,
        min_weeks_on_chart=5,
    )

    assert isinstance(result, models.Filter)
    assert result.must is not None
    assert len(result.must) == 3
    assert result.must[0].key == "community_tags"
    assert result.must[1].key == "chart_rank"
    assert result.must[2].key == "weeks_on_chart"
