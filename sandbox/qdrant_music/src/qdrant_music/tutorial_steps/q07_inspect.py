"""Q07 — Inspect segments and collection state."""

from qdrant_music.qdrant_ops import collection_summary
from qdrant_music.tutorial_steps.common import heading, show


def main() -> None:
    heading("Q07", "Inspect segments and collection state")
    show(collection_summary("baseline"))
    print(
        "\nA 50-point collection may show zero indexed vectors because a full scan "
        "is cheaper than building and traversing HNSW."
    )


if __name__ == "__main__":
    main()
