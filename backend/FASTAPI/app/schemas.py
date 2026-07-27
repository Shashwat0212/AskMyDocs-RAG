"""Request and response models used by the practice API."""

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Stable response returned by the health endpoint."""

    status: str
    environment: str


class ItemCreate(BaseModel):
    """Validated JSON body for creating an item."""

    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)


class ItemResponse(ItemCreate):
    """Item representation returned by the API."""

    id: int
