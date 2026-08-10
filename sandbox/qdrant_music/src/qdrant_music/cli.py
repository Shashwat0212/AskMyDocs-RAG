"""Command-line entrypoint for the RAG-002 learning sandbox."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from qdrant_music.dataset import load_dataset, validation_summary
from qdrant_music.qdrant_ops import (
    collection_name,
    collection_summary,
    create_payload_indexes,
    delete_collection,
    delete_point,
    ensure_collection,
    load_songs,
    search,
    update_review_note,
    wait_for_index,
    wait_until_ready,
)


def _print(value: Any) -> None:
    print(json.dumps(value, indent=2, default=str))


def _song_id_for_rank(rank: int) -> str:
    _, songs = load_dataset()
    for song in songs:
        if song.chart_rank == rank:
            return song.point_id
    raise ValueError(f"No frozen song has chart rank {rank}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="qdrant-music",
        description="RAG-002 local Qdrant internals learning sandbox",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    ready = subparsers.add_parser("wait-ready", help="Wait for Qdrant /readyz")
    ready.add_argument("--timeout", type=float, default=30.0)

    dataset = subparsers.add_parser("dataset", help="Dataset operations")
    dataset_subparsers = dataset.add_subparsers(dest="dataset_command", required=True)
    dataset_subparsers.add_parser("validate", help="Validate the frozen top-50 fixture")

    collection = subparsers.add_parser("collection", help="Collection operations")
    collection_subparsers = collection.add_subparsers(
        dest="collection_command",
        required=True,
    )
    for name in ("create", "load", "inspect", "delete"):
        child = collection_subparsers.add_parser(name)
        child.add_argument("--kind", choices=("baseline", "hnsw"), default="baseline")
    wait_index = collection_subparsers.add_parser("wait-index")
    wait_index.add_argument("--timeout", type=float, default=60.0)
    indexes = collection_subparsers.add_parser("create-payload-indexes")
    indexes.add_argument("--kind", choices=("baseline", "hnsw"), default="baseline")

    search_parser = subparsers.add_parser("search", help="Run a liking query")
    search_parser.add_argument("--query", required=True)
    search_parser.add_argument("--kind", choices=("baseline", "hnsw"), default="baseline")
    search_parser.add_argument("--limit", type=int, default=5)
    search_parser.add_argument("--score-threshold", type=float)
    search_parser.add_argument("--hnsw-ef", type=int)
    search_parser.add_argument("--exact", action="store_true")
    search_parser.add_argument("--tag")
    search_parser.add_argument("--max-chart-rank", type=int)
    search_parser.add_argument("--min-weeks", type=int)
    search_parser.add_argument("--with-vectors", action="store_true")

    point = subparsers.add_parser("point", help="Point mutation demonstrations")
    point_subparsers = point.add_subparsers(dest="point_command", required=True)
    delete = point_subparsers.add_parser("delete")
    delete.add_argument("--rank", type=int, required=True)
    delete.add_argument("--kind", choices=("baseline", "hnsw"), default="baseline")
    note = point_subparsers.add_parser("note")
    note.add_argument("--rank", type=int, required=True)
    note.add_argument("--text", required=True)
    note.add_argument("--kind", choices=("baseline", "hnsw"), default="baseline")

    return parser


def run(args: argparse.Namespace) -> int:
    if args.command == "wait-ready":
        _print(wait_until_ready(args.timeout))
    elif args.command == "dataset":
        _print(validation_summary())
    elif args.command == "collection":
        kind = getattr(args, "kind", "hnsw")
        if args.collection_command == "create":
            _print({"collection": ensure_collection(kind), "created_or_verified": True})
        elif args.collection_command == "load":
            _print(load_songs(kind))
        elif args.collection_command == "inspect":
            _print(collection_summary(kind))
        elif args.collection_command == "delete":
            name = collection_name(kind)
            _print({"collection": name, "deleted": delete_collection(kind)})
        elif args.collection_command == "wait-index":
            _print(wait_for_index(timeout_seconds=args.timeout))
        elif args.collection_command == "create-payload-indexes":
            create_payload_indexes(kind)
            _print({"collection": collection_name(kind), "payload_indexes": "ready"})
    elif args.command == "search":
        _print(
            search(
                args.query,
                kind=args.kind,
                limit=args.limit,
                score_threshold=args.score_threshold,
                hnsw_ef=args.hnsw_ef,
                exact=args.exact,
                required_tag=args.tag,
                max_chart_rank=args.max_chart_rank,
                min_weeks_on_chart=args.min_weeks,
                with_vectors=args.with_vectors,
            )
        )
    elif args.command == "point":
        point_id = _song_id_for_rank(args.rank)
        if args.point_command == "delete":
            _print(
                {
                    "point_id": point_id,
                    "remaining_exact_count": delete_point(point_id, kind=args.kind),
                }
            )
        elif args.point_command == "note":
            update_review_note(point_id, args.text, kind=args.kind)
            _print({"point_id": point_id, "note_updated": True})
    return 0


def main() -> None:
    parser = build_parser()
    try:
        raise SystemExit(run(parser.parse_args()))
    except (ConnectionError, OSError, TimeoutError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
