"""Q02 — Connect and inspect the server."""

from qdrant_music.qdrant_ops import client, wait_until_ready
from qdrant_music.tutorial_steps.common import heading, show


def main() -> None:
    heading("Q02", "Connect and inspect the server")
    show(wait_until_ready())
    show({"collections": [item.name for item in client().get_collections().collections]})


if __name__ == "__main__":
    main()
