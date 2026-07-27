"""Health endpoint."""

from fastapi import APIRouter, Request

from app.schemas import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health(request: Request) -> HealthResponse:
    """Report that the process is running and expose its learning environment."""

    settings = request.app.state.settings
    return HealthResponse(status="ok", environment=settings.app_env)
