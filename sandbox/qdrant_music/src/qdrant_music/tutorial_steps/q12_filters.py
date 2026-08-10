"""Q12 — Add filters and payload indexes."""

from qdrant_music.qdrant_ops import create_payload_indexes, search
from qdrant_music.settings import DEFAULT_QUERY
from qdrant_music.tutorial_steps.common import heading, show


def main() -> None:
    heading("Q12", "Add filters and payload indexes")
    before = search(
        DEFAULT_QUERY,
        kind="hnsw",
        required_tag="dance-pop",
        max_chart_rank=40,
    )
    create_payload_indexes("hnsw")
    after = search(
        DEFAULT_QUERY,
        kind="hnsw",
        required_tag="dance-pop",
        max_chart_rank=40,
    )
    show({"before_index": before, "after_index": after})
    print("\nThe index changes execution cost, not filter meaning.")


if __name__ == "__main__":
    main()
