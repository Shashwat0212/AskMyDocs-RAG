"""Application assembly for the FastAPI fundamentals lab."""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.middleware import request_context_middleware
from app.routers import health, items
from app.settings import Settings
from app.store import ItemStore

logger = logging.getLogger(__name__)


def configure_logging(log_level: str) -> None:
    """Configure readable console logging for local experimentation."""

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    logging.getLogger().setLevel(log_level)


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build an isolated app instance so tests do not share state."""

    app_settings = settings or Settings()
    configure_logging(app_settings.log_level)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        app.state.settings = app_settings
        app.state.item_store = ItemStore()
        logger.info(
            "application_started app_name=%s environment=%s",
            app_settings.app_name,
            app_settings.app_env,
        )
        yield
        logger.info("application_stopped app_name=%s", app_settings.app_name)

    application = FastAPI(
        title=app_settings.app_name,
        version="0.1.0",
        description="A disposable local lab for learning FastAPI fundamentals.",
        lifespan=lifespan,
    )
    application.middleware("http")(request_context_middleware)
    application.include_router(health.router, prefix="/api/v1")
    application.include_router(items.router, prefix="/api/v1")
    return application


app = create_app()
