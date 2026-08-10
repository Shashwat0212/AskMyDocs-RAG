"""Small local embedding helper used only by the learning sandbox."""

from __future__ import annotations

from functools import lru_cache
from typing import Iterable

import numpy as np
from fastembed import TextEmbedding

from qdrant_music.settings import SETTINGS


@lru_cache(maxsize=1)
def embedding_model() -> TextEmbedding:
    return TextEmbedding(model_name=SETTINGS.model_name)


def _embed(texts: Iterable[str]) -> list[list[float]]:
    vectors = [
        np.asarray(vector, dtype=np.float32).tolist()
        for vector in embedding_model().embed(list(texts))
    ]
    for vector in vectors:
        if len(vector) != SETTINGS.vector_size:
            raise ValueError(
                f"Expected {SETTINGS.vector_size} dimensions, got {len(vector)}"
            )
    return vectors


def embed_documents(descriptions: Iterable[str]) -> list[list[float]]:
    return _embed(f"search_document: {text}" for text in descriptions)


def embed_query(query: str) -> list[float]:
    if not query.strip():
        raise ValueError("Query text must not be empty")
    return _embed([f"search_query: {query.strip()}"])[0]
