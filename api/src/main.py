from fastapi import FastAPI
from src.loggers.base import get_default_logger

app = FastAPI()

logger = get_default_logger()


@app.get("/")
async def root():
    """
    Root endpoint.
    """
    logger.info("Root endpoint called")
    return {"message": "Hello, World!"}
