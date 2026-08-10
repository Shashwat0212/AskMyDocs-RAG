"""Q15 — Verify persistence after the documented Compose restart."""

from qdrant_music.qdrant_ops import collection_summary, wait_until_ready
from qdrant_music.tutorial_steps.common import heading, show


def main() -> None:
    heading("Q15", "Verify persistence")
    show(wait_until_ready())
    summary = collection_summary("baseline")
    show(summary)
    if summary["exact_count"] != 50:
        raise SystemExit("Expected 50 points after restart")


if __name__ == "__main__":
    main()
