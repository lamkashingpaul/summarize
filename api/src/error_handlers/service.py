from fastapi import Request
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

from src.errors.models import (
    CustomDatabaseBadRequestException,
    CustomDatabaseException,
    CustomDatabaseNotFoundException,
    CustomHttpException,
)
from src.loggers.service import get_default_logger

logger = get_default_logger()


def handle_custom_database_exception_for_http(e: Exception, passthrough: bool = False):
    if not isinstance(e, CustomDatabaseException):
        if not passthrough:
            raise e
        return

    match e:
        case CustomDatabaseBadRequestException():
            raise CustomHttpException(
                status_code=400,
                detail=e.message,
            ) from e

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


async def custom_rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    response = JSONResponse(
        status_code=429,
        content={"detail": f"Rate limit exceeded: {exc.detail}"},
    )
    response = request.app.state.limiter._inject_headers(
        response, request.state.view_rate_limit
    )
    return response


async def custom_http_exception_handler(request: Request, exc: CustomHttpException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def global_exception_handler(request: Request, exc: Exception):
    logger.error(exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )
