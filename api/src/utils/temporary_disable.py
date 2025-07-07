from functools import wraps

from fastapi import HTTPException, status


def temporary_disable(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Endpoint temporarily disabled.",
        )

    return wrapper
