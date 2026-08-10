"""Q10 — Compare exact and approximate search."""

from __future__ import annotations

import time

from qdrant_music.qdrant_ops import search
from qdrant_music.settings import DEFAULT_QUERY
from qdrant_music.tutorial_steps.common import heading, show


def _timed(*, exact: bool, hnsw_ef: int | None) -> dict[str, object]:
    started = time.perf_counter()
    results = search(
        DEFAULT_QUERY,
        kind="hnsw",
        exact=exact,
        hnsw_ef=hnsw_ef,
    )
    return {
        "exact": exact,
        "hnsw_ef": hnsw_ef,
        "elapsed_ms": round((time.perf_counter() - started) * 1000, 3),
        "result_ids": [item["id"] for item in results],
        "titles": [item["title"] for item in results],
    }


def main() -> None:
    heading("Q10", "Compare exact and approximate search")
    runs = [_timed(exact=True, hnsw_ef=None)]
    runs.extend(_timed(exact=False, hnsw_ef=value) for value in (8, 32, 128))
    exact_ids = set(runs[0]["result_ids"])
    for run in runs:
        run["exact_top5_overlap"] = len(exact_ids.intersection(run["result_ids"]))
    show(runs)
    print("\nThese timings are educational, not capacity benchmarks.")


if __name__ == "__main__":
    main()
