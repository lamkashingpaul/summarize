from fastapi import Request, Response
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

from src.errors.models import (
    CustomDatabaseException,
    CustomDatabaseNotFoundException,
    CustomHttpException,
)


def handle_custom_database_exception_for_http(e: Exception, passthrough: bool = False):
    if not isinstance(e, CustomDatabaseException):
        if not passthrough:
            raise e
        return

    match e:
        case CustomDatabaseNotFoundException():
            raise CustomHttpException(
                status_code=404,
                detail=e.message,
            ) from e

        case _:
            raise CustomHttpException(
                status_code=500,
                detail="Internal Server Error",
            ) from e


async def custom_http_exception_handler(request: Request, exc: CustomHttpException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> Response:
    response = JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"},
    )
    response = request.app.state.limiter._inject_headers(
        response, request.state.view_rate_limit
    )
    return response


async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )
