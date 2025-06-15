import asyncio
from typing import Callable

from fastapi import Request, Response
from fastapi.routing import APIRoute

from src.errors.models import CustomHttpException


class CustomAPIRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await asyncio.wait_for(
                    original_route_handler(request), timeout=60
                )
            except asyncio.TimeoutError:
                raise CustomHttpException(
                    status_code=504,
                    detail="Request timed out after 60 seconds.",
                )

        return custom_route_handler

    def __hash__(self):
        return hash((self.endpoint))
