from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from src.articles.controller import articles_router
from src.error_handlers.service import (
    custom_http_exception_handler,
    global_exception_handler,
    rate_limit_exceeded_handler,
)
from src.errors.models import CustomHttpException
from src.health.controller import health_router
from src.question_and_answers.controller import question_and_answers_router
from src.rate_limiter.service import limiter
from src.settings.service import settings

app = FastAPI(root_path="/api")

api_v1 = FastAPI()
api_v1.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
api_v1.state.limiter = limiter
api_v1.add_middleware(SlowAPIMiddleware)

api_v1.include_router(health_router)
api_v1.include_router(articles_router)
api_v1.include_router(question_and_answers_router)

api_v1.exception_handlers[RateLimitExceeded] = rate_limit_exceeded_handler
api_v1.exception_handlers[CustomHttpException] = custom_http_exception_handler
api_v1.exception_handlers[Exception] = global_exception_handler

app.mount("/v1", api_v1)
