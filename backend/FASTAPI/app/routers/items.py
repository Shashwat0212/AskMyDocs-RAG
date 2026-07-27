"""In-memory item routes for practicing common API operations."""

from fastapi import APIRouter, HTTPException, Response, status

from app.dependencies import ItemStoreDependency, PaginationDependency
from app.schemas import ItemCreate, ItemResponse

router = APIRouter(prefix="/items", tags=["items"])


@router.post("", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    item: ItemCreate,
    store: ItemStoreDependency,
) -> ItemResponse:
    """Create an item after FastAPI validates the JSON request body."""

    return store.create(item)


@router.get("", response_model=list[ItemResponse])
async def list_items(
    pagination: PaginationDependency,
    store: ItemStoreDependency,
) -> list[ItemResponse]:
    """List items using validated, dependency-injected pagination."""

    return store.list(offset=pagination.offset, limit=pagination.limit)


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int, store: ItemStoreDependency) -> ItemResponse:
    """Fetch an item or raise an expected HTTP 404 error."""

    item = store.get(item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} was not found",
        )
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, store: ItemStoreDependency) -> Response:
    """Delete an item or raise an expected HTTP 404 error."""

    if not store.delete(item_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} was not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int,
    item_update: ItemCreate,
    store: ItemStoreDependency,
) -> ItemResponse:
    """Update an item or raise an expected HTTP 404 error."""

    item = store.update(item_id, item_update)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} was not found",
        )
    return item
