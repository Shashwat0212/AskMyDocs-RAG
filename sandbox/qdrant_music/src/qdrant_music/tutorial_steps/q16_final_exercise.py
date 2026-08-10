"""Q16 — Final exercise scaffold."""

from qdrant_music.qdrant_ops import search
from qdrant_music.tutorial_steps.common import heading, show


def main() -> None:
    heading("Q16", "Final exercise and cleanup")
    query = "confident high-energy music for a road trip"
    show(
        search(
            query,
            kind="hnsw",
            hnsw_ef=64,
            max_chart_rank=50,
            limit=5,
        )
    )
    print(
        "\nExercise: change the query and add either a tag or weeks-on-chart "
        "constraint. Explain the top three results using their tags."
    )


if __name__ == "__main__":
    main()
