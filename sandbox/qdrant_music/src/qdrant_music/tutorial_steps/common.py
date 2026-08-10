"""Presentation helpers for numbered tutorial programs."""

from __future__ import annotations

import json
from typing import Any


def heading(phase: str, title: str) -> None:
    print(f"\n{phase} — {title}\n{'=' * (len(phase) + len(title) + 3)}")


def show(value: Any) -> None:
    print(json.dumps(value, indent=2, default=str))
