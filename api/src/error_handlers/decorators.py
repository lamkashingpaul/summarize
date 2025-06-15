from functools import wraps

from src.database.service import SessionDep
from src.error_handlers.service import handle_custom_database_exception_for_http
from src.utils.retrieve_target_from_kwargs import retrieve_target_from_kwargs


def custom_exception_handler_for_http(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        session = retrieve_target_from_kwargs(func, kwargs, target_type=SessionDep)

        try:
            return await func(*args, **kwargs)

        except Exception as e:
            if session:
                await session.rollback()

            handle_custom_database_exception_for_http(e, passthrough=True)

            raise e

    return wrapper
