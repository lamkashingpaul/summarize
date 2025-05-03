from fastapi import FastAPI
from src.settings.service import settings
from src.loggers.service import get_default_logger
from src.health.controller import health_router
from src.articles.controller import articles_router

app = FastAPI()

logger = get_default_logger()

app.include_router(health_router)

app.include_router(articles_router)


@app.get("/")
async def root():
    return settings
