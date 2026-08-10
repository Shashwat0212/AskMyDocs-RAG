"""Q08 — Run exact similarity search."""

from qdrant_music.qdrant_ops import search
from qdrant_music.settings import DEFAULT_QUERY
from qdrant_music.tutorial_steps.common import heading, show


def main() -> None:
    heading("Q08", "Run exact similarity search")
    show(search(DEFAULT_QUERY, exact=True))


if __name__ == "__main__":
    main()
