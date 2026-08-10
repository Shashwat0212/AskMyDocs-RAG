"""Frozen Billboard dataset loading, validation, and payload conversion."""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from qdrant_music.settings import SETTINGS


class DatasetValidationError(ValueError):
    """Raised when the immutable learning fixture is malformed."""


@dataclass(frozen=True)
class Song:
    chart_rank: int
    last_week: int | None
    peak_rank: int
    weeks_on_chart: int
    title: str
    artist: str
    community_tags: tuple[str, ...]
    description: str
    tag_source: str
    review_status: str

    @property
    def point_id(self) -> str:
        seed = f"billboard-hot-100|2024-06-01|{self.chart_rank}|{self.title}|{self.artist}"
        return str(uuid.uuid5(uuid.NAMESPACE_URL, seed))

    def payload(self, metadata: dict[str, Any]) -> dict[str, Any]:
        return {
            "chart_name": metadata["chart_name"],
            "chart_date": metadata["chart_date"],
            "chart_rank": self.chart_rank,
            "last_week": self.last_week,
            "peak_rank": self.peak_rank,
            "weeks_on_chart": self.weeks_on_chart,
            "title": self.title,
            "artist": self.artist,
            "community_tags": list(self.community_tags),
            "description": self.description,
            "tag_source": self.tag_source,
            "review_status": self.review_status,
            "chart_source_url": metadata["chart_source_url"],
        }


def file_sha256(path: Path = SETTINGS.dataset_path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_dataset(path: Path = SETTINGS.dataset_path) -> tuple[dict[str, Any], list[Song]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    metadata = raw["metadata"]
    songs = [
        Song(
            chart_rank=item["chart_rank"],
            last_week=item["last_week"],
            peak_rank=item["peak_rank"],
            weeks_on_chart=item["weeks_on_chart"],
            title=item["title"],
            artist=item["artist"],
            community_tags=tuple(item["community_tags"]),
            description=item["description"],
            tag_source=item["tag_source"],
            review_status=item["review_status"],
        )
        for item in raw["songs"]
    ]
    validate_dataset(metadata, songs)
    return metadata, songs


def validate_dataset(metadata: dict[str, Any], songs: list[Song]) -> None:
    errors: list[str] = []
    ranks = [song.chart_rank for song in songs]
    ids = [song.point_id for song in songs]

    if metadata.get("chart_name") != "Billboard Hot 100":
        errors.append("chart_name must be 'Billboard Hot 100'")
    if metadata.get("chart_date") != "2024-06-01":
        errors.append("chart_date must match the frozen 2024-06-01 snapshot")
    if len(songs) != 50:
        errors.append(f"expected 50 songs, found {len(songs)}")
    if sorted(ranks) != list(range(1, 51)):
        errors.append("chart ranks must be exactly 1 through 50")
    if len(ids) != len(set(ids)):
        errors.append("stable point IDs must be unique")

    for song in songs:
        if not 1 <= song.peak_rank <= song.chart_rank:
            errors.append(f"invalid peak rank for {song.title}")
        if song.weeks_on_chart < 1:
            errors.append(f"weeks_on_chart must be positive for {song.title}")
        if len(song.community_tags) < 2:
            errors.append(f"at least two community tags required for {song.title}")
        if len(song.description.strip()) < 30:
            errors.append(f"description is too short for {song.title}")
        if song.review_status != "manually_reviewed":
            errors.append(f"{song.title} must be manually reviewed")

    if errors:
        raise DatasetValidationError("; ".join(errors))


def validation_summary(path: Path = SETTINGS.dataset_path) -> dict[str, Any]:
    metadata, songs = load_dataset(path)
    checksum = file_sha256(path)
    if path == SETTINGS.dataset_path and checksum != SETTINGS.dataset_sha256:
        raise DatasetValidationError(
            "Dataset checksum changed; review provenance and update shared settings"
        )
    return {
        "chart": metadata["chart_name"],
        "chart_date": metadata["chart_date"],
        "records": len(songs),
        "rank_min": min(song.chart_rank for song in songs),
        "rank_max": max(song.chart_rank for song in songs),
        "duplicate_ids": len(songs) - len({song.point_id for song in songs}),
        "missing_descriptions": sum(not song.description for song in songs),
        "sha256": checksum,
        "valid": True,
    }
