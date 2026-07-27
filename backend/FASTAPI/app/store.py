"""A deliberately simple in-memory store for practicing API behavior."""

from app.schemas import ItemCreate, ItemResponse


class ItemStore:
    """Store items for the lifetime of one application instance."""

    def __init__(self) -> None:
        self._items: dict[int, ItemResponse] = {}
        self._next_id = 1

    def create(self, item: ItemCreate) -> ItemResponse:
        created = ItemResponse(id=self._next_id, **item.model_dump())
        self._items[created.id] = created
        self._next_id += 1
        return created

    def list(self, *, offset: int, limit: int) -> list[ItemResponse]:
        items = list(self._items.values())
        return items[offset : offset + limit]

    def get(self, item_id: int) -> ItemResponse | None:
        return self._items.get(item_id)

    def delete(self, item_id: int) -> bool:
        return self._items.pop(item_id, None) is not None

    def update(self, item_id: int, item_update: ItemCreate) -> ItemResponse | None:
        existing_item = self._items.get(item_id)
        if existing_item is None:
            return None
        updated_item = ItemResponse(id=item_id, **item_update.model_dump())
        self._items[item_id] = updated_item
        return updated_item
