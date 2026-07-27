"""Convenient ASGI entrypoint for running the learning lab from this directory."""

from app.main import app, create_app

__all__ = ["app", "create_app"]
