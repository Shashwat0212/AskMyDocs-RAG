"""Q04 — Generate and inspect an embedding."""

import math

from qdrant_music.dataset import load_dataset
from qdrant_music.embedding import embed_documents
from qdrant_music.tutorial_steps.common import heading, show


def main() -> None:
    heading("Q04", "Generate and inspect an embedding")
    _, songs = load_dataset()
    vector = embed_documents([songs[0].description])[0]
    show(
        {
            "song": songs[0].title,
            "dimensions": len(vector),
            "l2_norm": math.sqrt(sum(value * value for value in vector)),
            "first_five_values": vector[:5],
        }
    )


if __name__ == "__main__":
    main()
