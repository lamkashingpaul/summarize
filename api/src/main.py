from fastapi import FastAPI

from src.articles.controller import articles_router
from src.health.controller import health_router
from src.loggers.service import get_default_logger
from src.question_and_answers.controller import question_and_answers_router
from src.settings.service import settings

app = FastAPI()

logger = get_default_logger()

app.include_router(health_router)

app.include_router(articles_router)

app.include_router(question_and_answers_router)


@app.get("/")
async def root():
    return settings
