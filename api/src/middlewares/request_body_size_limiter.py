from fastapi.responses import JSONResponse
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp, Message

from src.errors.models import CustomHttpException


class RequestBodySizeLimiter(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, max_size_bytes: int = 1024 * 1024):  # Default 1MB
        super().__init__(app)
        self.max_size_bytes = max_size_bytes

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        try:
            if not self.is_json_request(request):
                return await call_next(request)

            if content_length := request.headers.get("Content-Length"):
                try:
                    if int(content_length) > self.max_size_bytes:
                        raise CustomHttpException(
                            status_code=413,
                            detail=f"Payload too large (max {self.max_size_bytes} bytes)",
                        )
                except ValueError:
                    raise CustomHttpException(
                        400,
                        "Invalid Content-Length header",
                    )

            received_bytes = 0
            original_receive = request._receive

            async def receive_wrapper() -> Message:
                nonlocal received_bytes

                message = await original_receive()
                if message["type"] != "http.request":
                    return message

                body = message.get("body", b"")
                received_bytes += len(body)

                if received_bytes > self.max_size_bytes:
                    raise CustomHttpException(
                        status_code=413, detail="Streaming body exceeded size limit"
                    )

                return message

            request._receive = receive_wrapper

            response = await call_next(request)
            return response
        except CustomHttpException as e:
            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail},
            )
        except Exception as e:
            raise e

    def is_json_request(self, request: Request) -> bool:
        content_type = request.headers.get("Content-Type", "").lower()
        return (
            "application/json" in content_type
            or "application/x-json" in content_type
            or "text/json" in content_type
        )
