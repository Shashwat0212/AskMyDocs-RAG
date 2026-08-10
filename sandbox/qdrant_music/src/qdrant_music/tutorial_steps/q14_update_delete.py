"""Q14 — Update, delete, and restore a point."""

from qdrant_music.dataset import load_dataset
from qdrant_music.qdrant_ops import delete_point, load_songs, update_review_note
from qdrant_music.tutorial_steps.common import heading, show


def main() -> None:
    heading("Q14", "Update, delete, and restore a point")
    _, songs = load_dataset()
    point_id = songs[0].point_id
    update_review_note(point_id, "Updated during tutorial Q14")
    remaining = delete_point(point_id)
    restored = load_songs("baseline")
    show(
        {
            "mutated_point_id": point_id,
            "count_after_delete": remaining,
            "count_after_idempotent_restore": restored["exact_count"],
        }
    )


if __name__ == "__main__":
    main()
