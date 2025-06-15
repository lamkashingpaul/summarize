import json
import time
from collections.abc import Buffer
from typing import Optional, cast

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.concurrency import iterate_in_threadpool
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.routing import APIRoute
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from src.analytics.schemas.internals import CreateRequestLogDto
from src.analytics.tasks import save_request_log_task
from src.errors.models import CustomHttpException
from src.utils.metadata import LOG_METADATA_KEY, LoggingMetadata


class RequestAndResponseLogger(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)
        self.logging_routes = None

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if self.logging_routes is None:
            self.logging_routes = self.get_logging_routes(request.app)

        request_body, request_body_error = await self.extract_request_body(request)
        response = None
        errors: list[str] = []
        start_time = time.perf_counter()

        try:
            response = await call_next(request)
            return response

        except (HTTPException, CustomHttpException) as e:
            response = JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail},
            )
            errors.append(str(e.detail))
            return response

        except Exception as e:
            response = JSONResponse(
                status_code=500,
                content={"detail": "Internal Server Error"},
            )
            errors.append(str(e))
            return response

        finally:
            if self.should_log_request(request):
                duration_ms = (time.perf_counter() - start_time) * 1000
                log_data = await self.prepare_log_data(
                    request,
                    response,
                    request_body,
                    request_body_error,
                    duration_ms,
                    errors,
                )

                if response is not None:
                    if not isinstance(response.background, BackgroundTasks):
                        response.background = BackgroundTasks()
                    response.background.add_task(
                        save_request_log_task, CreateRequestLogDto(**log_data)
                    )

    async def prepare_log_data(
        self,
        request: Request,
        response: Optional[Response],
        request_body: dict,
        request_body_error: str,
        duration_ms: float,
        errors: list[str],
    ) -> dict:
        response_body, response_body_error = await self.extract_response_body(response)
        if response_body_error:
            errors.append(response_body_error)
        if request_body_error:
            errors.append(request_body_error)

        return {
            "client_ip": request.client and request.client.host or "unknown",
            "method": request.method,
            "path": request.url.path,
            "query_params": dict(request.query_params),
            "request_header": dict(request.headers),
            "request_body": request_body,
            "response_status": response.status_code if response else 500,
            "response_header": dict(response.headers) if response else {},
            "response_body": response_body,
            "duration_ms": duration_ms,
            "error": "; ".join(errors),
        }

    async def extract_request_body(self, request: Request) -> tuple[dict, str]:
        try:
            content_type = request.headers.get("content-type", "")
            if "application/json" not in content_type:
                return {}, ""

            request_body = await request.body()
            request_body = json.loads(request_body.decode("utf-8"))
            return request_body, ""

        except json.JSONDecodeError:
            return {}, "Invalid JSON body"
        except Exception as e:
            return {}, f"Error extracting request body: {str(e)}"

    async def extract_response_body(
        self, response: Optional[Response]
    ) -> tuple[dict, str]:
        try:
            if response is None or "application/json" not in response.headers.get(
                "content-type", ""
            ):
                return {}, ""

            if hasattr(response, "body"):
                response_body = response.body
                if isinstance(response_body, memoryview):
                    response_body = response_body.tobytes()
            elif hasattr(response, "body_iterator"):
                streaming_response = cast(StreamingResponse, response)
                response_body = [
                    chunk async for chunk in streaming_response.body_iterator
                ]
                streaming_response.body_iterator = iterate_in_threadpool(
                    iter(response_body)
                )
                response_body = b"".join(cast(list[Buffer], response_body))

            response_body = json.loads(response_body.decode("utf-8"))
            return response_body, ""

        except json.JSONDecodeError:
            return {}, "Invalid JSON body"
        except Exception as e:
            return {}, f"Error extracting response body: {str(e)}"

    def should_log_request(self, request: Request) -> bool:
        if not self.logging_routes:
            return False
        return request.scope.get("route") in self.logging_routes

    def get_logging_routes(self, app: FastAPI) -> set[APIRoute]:
        logging_routes: set[APIRoute] = set()

        for route in app.routes:
            if not isinstance(route, APIRoute):
                continue

            endpoint = route.endpoint
            current = endpoint
            while current is not None:
                metadata = getattr(current, LOG_METADATA_KEY, None)
                if isinstance(metadata, LoggingMetadata) and metadata.enabled:
                    logging_routes.add(route)
                current = getattr(current, "__wrapped__", None)

        return logging_routes
