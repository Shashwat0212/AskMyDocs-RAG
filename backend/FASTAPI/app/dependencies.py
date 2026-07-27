"""Reusable FastAPI dependencies for the learning lab."""

from typing import Annotated

from fastapi import Depends, Query, Request
from pydantic import BaseModel

from app.store import ItemStore


class Pagination(BaseModel):
    """Validated pagination values shared by list endpoints."""

    offset: int
    limit: int


def pagination_parameters(
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> Pagination:
    return Pagination(offset=offset, limit=limit)


PaginationDependency = Annotated[Pagination, Depends(pagination_parameters)]


def get_item_store(request: Request) -> ItemStore:
    """Fetch lifespan-managed state from the current app instance."""

    return request.app.state.item_store


ItemStoreDependency = Annotated[ItemStore, Depends(get_item_store)]
