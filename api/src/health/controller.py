from fastapi import APIRouter

from src.health.schemas.responses import HealthCheckResponse
from src.utils.custom_api_route import CustomAPIRoute

health_router = APIRouter(
    prefix="/health",
    tags=["health"],
    route_class=CustomAPIRoute,
)


@health_router.get("")
async def health_check() -> HealthCheckResponse:
    return HealthCheckResponse(status="ok")
