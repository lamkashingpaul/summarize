from functools import wraps

from src.utils.metadata import LOG_METADATA_KEY, LoggingMetadata


def log_request_response(func):
    setattr(func, LOG_METADATA_KEY, LoggingMetadata(enabled=True))

    @wraps(func)
    async def wrapper(*arg, **kwargs):
        return await func(*arg, **kwargs)

    return wrapper
