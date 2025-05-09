import inspect
from functools import wraps
from typing import cast

from src.database.service import SessionDep
from src.error_handlers.service import handle_custom_database_exception_for_http


def custom_exception_handler_for_http(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        session = None

        for param in sig.parameters.values():
            name = param.name
            annotation = param.annotation
            if annotation == SessionDep:
                session = kwargs.get(name)
                session = session or next(
                    (arg for arg in args if isinstance(arg, annotation))
                )
                session = cast(SessionDep, session)
                break

        try:
            return await func(*args, **kwargs)
        except Exception as e:
            if session:
                await session.rollback()

            handle_custom_database_exception_for_http(e, passthrough=True)

            raise e

    return wrapper
