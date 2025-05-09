from fastapi import Request
from fastapi.responses import JSONResponse

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
                detail={"message": e.message},
            ) from e

        case _:
            raise CustomHttpException(
                status_code=500,
                detail={"message": "Internal Server Error"},
            ) from e


async def custom_http_exception_handler(request: Request, exc: CustomHttpException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": {"message": "Internal Server Error"}},
    )
