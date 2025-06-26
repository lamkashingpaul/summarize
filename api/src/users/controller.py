from fastapi import APIRouter

from src.users.schemas.response import GetAuthenticatedUserResponse
from src.utils.custom_api_route import CustomAPIRoute

users_router = APIRouter(
    prefix="/users",
    tags=["users"],
    route_class=CustomAPIRoute,
)


@users_router.get("/me", status_code=200)
async def get_authenticated_user() -> GetAuthenticatedUserResponse:
    return GetAuthenticatedUserResponse(
        email="foo@bar.com",
        name="Foo Bar",
        image_url="https://example.com/image.jpg",
        is_email_verified=True,
    )
