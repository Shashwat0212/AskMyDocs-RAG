"""Q03 — Inspect and validate Billboard data."""

from qdrant_music.dataset import load_dataset, validation_summary
from qdrant_music.tutorial_steps.common import heading, show


def main() -> None:
    heading("Q03", "Inspect and validate Billboard data")
    show(validation_summary())
    _, songs = load_dataset()
    show(
        [
            {
                "rank": song.chart_rank,
                "title": song.title,
                "artist": song.artist,
                "tags": song.community_tags,
            }
            for song in songs[:3]
        ]
    )


if __name__ == "__main__":
    main()
