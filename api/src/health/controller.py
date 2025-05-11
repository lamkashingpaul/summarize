from fastapi import APIRouter

from src.health.schemas import HealthCheckResponse

health_router = APIRouter(prefix="/health", tags=["health"])


@health_router.get("")
async def health_check() -> HealthCheckResponse:
    return HealthCheckResponse(status="ok")
