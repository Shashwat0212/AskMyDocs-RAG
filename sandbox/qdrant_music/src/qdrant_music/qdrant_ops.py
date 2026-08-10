"""Qdrant operations shared by the CLI, tutorial programs, and notebook."""

from __future__ import annotations

import time
import urllib.error
import urllib.request
from collections.abc import Iterable
from typing import Any, Literal

from qdrant_client import QdrantClient, models

from qdrant_music.dataset import Song, load_dataset
from qdrant_music.embedding import embed_documents, embed_query
from qdrant_music.settings import SETTINGS

CollectionKind = Literal["baseline", "hnsw"]


def client() -> QdrantClient:
    return QdrantClient(url=SETTINGS.qdrant_url, timeout=30)


def wait_until_ready(timeout_seconds: float = 30.0) -> dict[str, str]:
    deadline = time.monotonic() + timeout_seconds
    ready_url = f"{SETTINGS.qdrant_url.rstrip('/')}/readyz"
    last_error = "not attempted"
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(ready_url, timeout=2) as response:
                if response.status == 200:
                    return {"url": ready_url, "status": "ready"}
        except (OSError, urllib.error.URLError) as error:
            last_error = str(error)
        time.sleep(0.5)
    raise TimeoutError(
        f"Qdrant was not ready at {ready_url} within {timeout_seconds}s: {last_error}"
    )


def collection_name(
    kind: CollectionKind,
    *,
    notebook: bool = False,
) -> str:
    if notebook:
        return (
            SETTINGS.notebook_baseline_collection
            if kind == "baseline"
            else SETTINGS.notebook_hnsw_collection
        )
    return SETTINGS.baseline_collection if kind == "baseline" else SETTINGS.hnsw_collection


def _vector_params(info: Any) -> Any:
    vectors = info.config.params.vectors
    if isinstance(vectors, dict):
        if "" in vectors:
            return vectors[""]
        if len(vectors) == 1:
            return next(iter(vectors.values()))
        raise ValueError("Tutorial expects one unnamed dense vector")
    return vectors


def ensure_collection(
    kind: CollectionKind,
    *,
    notebook: bool = False,
) -> str:
    qdrant = client()
    name = collection_name(kind, notebook=notebook)

    if qdrant.collection_exists(name):
        info = qdrant.get_collection(name)
        vector_params = _vector_params(info)
        if vector_params.size != SETTINGS.vector_size:
            raise ValueError(
                f"Collection {name} has size {vector_params.size}; "
                f"expected {SETTINGS.vector_size}. Delete it explicitly before retrying."
            )
        if vector_params.distance != models.Distance.COSINE:
            raise ValueError(
                f"Collection {name} does not use cosine distance. "
                "Delete it explicitly before retrying."
            )
        return name

    kwargs: dict[str, Any] = {}
    if kind == "hnsw":
        kwargs["hnsw_config"] = models.HnswConfigDiff(
            m=SETTINGS.hnsw_m,
            ef_construct=SETTINGS.hnsw_ef_construct,
            full_scan_threshold=SETTINGS.hnsw_full_scan_threshold_kb,
        )
        kwargs["optimizers_config"] = models.OptimizersConfigDiff(
            indexing_threshold=SETTINGS.indexing_threshold_kb,
        )

    qdrant.create_collection(
        collection_name=name,
        vectors_config=models.VectorParams(
            size=SETTINGS.vector_size,
            distance=models.Distance.COSINE,
        ),
        **kwargs,
    )
    return name


def build_points(
    songs: Iterable[Song],
    metadata: dict[str, Any],
) -> list[models.PointStruct]:
    song_list = list(songs)
    vectors = embed_documents(song.description for song in song_list)
    return [
        models.PointStruct(
            id=song.point_id,
            vector=vector,
            payload=song.payload(metadata),
        )
        for song, vector in zip(song_list, vectors, strict=True)
    ]


def load_songs(
    kind: CollectionKind,
    *,
    notebook: bool = False,
) -> dict[str, Any]:
    metadata, songs = load_dataset()
    name = ensure_collection(kind, notebook=notebook)
    points = build_points(songs, metadata)
    qdrant = client()
    qdrant.upsert(collection_name=name, points=points, wait=True)
    exact_count = qdrant.count(collection_name=name, exact=True).count
    return {"collection": name, "upserted": len(points), "exact_count": exact_count}


def collection_summary(
    kind: CollectionKind,
    *,
    notebook: bool = False,
) -> dict[str, Any]:
    name = collection_name(kind, notebook=notebook)
    qdrant = client()
    info = qdrant.get_collection(name)
    vector_params = _vector_params(info)
    return {
        "collection": name,
        "status": str(info.status),
        "optimizer_status": str(info.optimizer_status),
        "points_count_approximate": info.points_count,
        "indexed_vectors_count_approximate": info.indexed_vectors_count,
        "exact_count": qdrant.count(collection_name=name, exact=True).count,
        "segments_count": info.segments_count,
        "vector_size": vector_params.size,
        "distance": str(vector_params.distance),
        "hnsw_m": info.config.hnsw_config.m,
        "hnsw_ef_construct": info.config.hnsw_config.ef_construct,
        "full_scan_threshold_kb": info.config.hnsw_config.full_scan_threshold,
        "indexing_threshold_kb": info.config.optimizer_config.indexing_threshold,
    }


def wait_for_index(
    *,
    notebook: bool = False,
    timeout_seconds: float = 60.0,
) -> dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    last_summary: dict[str, Any] = {}
    while time.monotonic() < deadline:
        last_summary = collection_summary("hnsw", notebook=notebook)
        indexed = last_summary["indexed_vectors_count_approximate"] or 0
        if indexed >= 50:
            return last_summary
        time.sleep(1)
    raise TimeoutError(
        "HNSW index did not report 50 indexed vectors before timeout. "
        f"Last collection state: {last_summary}"
    )


def build_filter(
    *,
    required_tag: str | None = None,
    max_chart_rank: int | None = None,
    min_weeks_on_chart: int | None = None,
) -> models.Filter | None:
    conditions: list[models.Condition] = []
    if required_tag:
        conditions.append(
            models.FieldCondition(
                key="community_tags",
                match=models.MatchValue(value=required_tag),
            )
        )
    if max_chart_rank is not None:
        conditions.append(
            models.FieldCondition(
                key="chart_rank",
                range=models.Range(lte=max_chart_rank),
            )
        )
    if min_weeks_on_chart is not None:
        conditions.append(
            models.FieldCondition(
                key="weeks_on_chart",
                range=models.Range(gte=min_weeks_on_chart),
            )
        )
    return models.Filter(must=conditions) if conditions else None


def search(
    query: str,
    *,
    kind: CollectionKind = "baseline",
    notebook: bool = False,
    limit: int = 5,
    score_threshold: float | None = None,
    hnsw_ef: int | None = None,
    exact: bool = False,
    required_tag: str | None = None,
    max_chart_rank: int | None = None,
    min_weeks_on_chart: int | None = None,
    with_vectors: bool = False,
) -> list[dict[str, Any]]:
    query_vector = embed_query(query)
    response = client().query_points(
        collection_name=collection_name(kind, notebook=notebook),
        query=query_vector,
        query_filter=build_filter(
            required_tag=required_tag,
            max_chart_rank=max_chart_rank,
            min_weeks_on_chart=min_weeks_on_chart,
        ),
        search_params=models.SearchParams(hnsw_ef=hnsw_ef, exact=exact),
        limit=limit,
        score_threshold=score_threshold,
        with_payload=True,
        with_vectors=with_vectors,
    )
    return [
        {
            "id": str(point.id),
            "score": point.score,
            "title": point.payload["title"],
            "artist": point.payload["artist"],
            "chart_rank": point.payload["chart_rank"],
            "weeks_on_chart": point.payload["weeks_on_chart"],
            "community_tags": point.payload["community_tags"],
            "description": point.payload["description"],
            "vector_returned": point.vector is not None,
        }
        for point in response.points
    ]


def create_payload_indexes(
    kind: CollectionKind,
    *,
    notebook: bool = False,
) -> None:
    qdrant = client()
    name = collection_name(kind, notebook=notebook)
    fields = {
        "community_tags": models.PayloadSchemaType.KEYWORD,
        "chart_rank": models.PayloadSchemaType.INTEGER,
        "weeks_on_chart": models.PayloadSchemaType.INTEGER,
        "chart_date": models.PayloadSchemaType.DATETIME,
    }
    for field_name, schema in fields.items():
        qdrant.create_payload_index(
            collection_name=name,
            field_name=field_name,
            field_schema=schema,
            wait=True,
        )


def delete_point(
    point_id: str,
    *,
    kind: CollectionKind = "baseline",
    notebook: bool = False,
) -> int:
    name = collection_name(kind, notebook=notebook)
    qdrant = client()
    qdrant.delete(
        collection_name=name,
        points_selector=models.PointIdsList(points=[point_id]),
        wait=True,
    )
    return qdrant.count(collection_name=name, exact=True).count


def update_review_note(
    point_id: str,
    note: str,
    *,
    kind: CollectionKind = "baseline",
    notebook: bool = False,
) -> None:
    client().set_payload(
        collection_name=collection_name(kind, notebook=notebook),
        payload={"tutorial_review_note": note},
        points=[point_id],
        wait=True,
    )


def delete_collection(
    kind: CollectionKind,
    *,
    notebook: bool = False,
) -> bool:
    name = collection_name(kind, notebook=notebook)
    qdrant = client()
    if not qdrant.collection_exists(name):
        return False
    qdrant.delete_collection(name)
    return True
