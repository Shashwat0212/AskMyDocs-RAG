"""Q05 — Create the baseline collection."""

from qdrant_music.qdrant_ops import collection_summary, ensure_collection
from qdrant_music.tutorial_steps.common import heading, show


def main() -> None:
    heading("Q05", "Create the baseline collection")
    ensure_collection("baseline")
    show(collection_summary("baseline"))


if __name__ == "__main__":
    main()
