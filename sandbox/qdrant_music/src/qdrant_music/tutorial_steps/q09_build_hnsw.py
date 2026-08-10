"""Q09 — Build the HNSW learning collection."""

from qdrant_music.qdrant_ops import load_songs, wait_for_index
from qdrant_music.tutorial_steps.common import heading, show


def main() -> None:
    heading("Q09", "Build the HNSW learning collection")
    show(load_songs("hnsw"))
    show(wait_for_index())


if __name__ == "__main__":
    main()
