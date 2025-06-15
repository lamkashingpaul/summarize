from src.analytics.models.request_log import RequestLog
from src.analytics.schemas.internals import CreateRequestLogDto
from src.database.service import SessionDep


async def save_request_log(
    create_request_log_dto: CreateRequestLogDto,
    session: SessionDep,
) -> RequestLog:
    request_log = RequestLog(**create_request_log_dto.model_dump())
    session.add(request_log)
    return request_log
