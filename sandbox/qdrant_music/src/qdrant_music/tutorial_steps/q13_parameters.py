"""Q13 — Explore parameter trade-offs."""

from qdrant_music.qdrant_ops import search
from qdrant_music.settings import DEFAULT_QUERY
from qdrant_music.tutorial_steps.common import heading, show


def main() -> None:
    heading("Q13", "Explore parameter trade-offs")
    runs = []
    for hnsw_ef in (8, 32, 128):
        results = search(
            DEFAULT_QUERY,
            kind="hnsw",
            hnsw_ef=hnsw_ef,
            score_threshold=0.2,
            limit=5,
        )
        runs.append(
            {
                "hnsw_ef": hnsw_ef,
                "returned": len(results),
                "top_title": results[0]["title"] if results else None,
                "lowest_returned_score": results[-1]["score"] if results else None,
            }
        )
    show(runs)
    print(
        "\nHigher hnsw_ef explores more graph candidates. This tiny collection "
        "is for learning controls, not benchmarking capacity."
    )


if __name__ == "__main__":
    main()
