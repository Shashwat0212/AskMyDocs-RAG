"""Q06 — Trace and execute an upsert."""

from qdrant_music.qdrant_ops import load_songs
from qdrant_music.tutorial_steps.common import heading, show


def main() -> None:
    heading("Q06", "Trace and execute an upsert")
    show(load_songs("baseline"))


if __name__ == "__main__":
    main()
