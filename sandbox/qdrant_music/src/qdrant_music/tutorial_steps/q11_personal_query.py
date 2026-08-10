"""Q11 — Run a personal liking query."""

import argparse

from qdrant_music.qdrant_ops import search
from qdrant_music.tutorial_steps.common import heading, show


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--query",
        default="melancholic acoustic songs with calm intimate vocals",
    )
    args = parser.parse_args()
    heading("Q11", "Run a personal liking query")
    show(search(args.query, kind="hnsw", hnsw_ef=64))


if __name__ == "__main__":
    main()
