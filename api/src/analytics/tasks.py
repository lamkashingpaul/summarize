from src.analytics.schemas.internals import CreateRequestLogDto
from src.analytics.service import save_request_log
from src.database.service import AsyncSessionLocal


async def save_request_log_task(create_request_log_dto: CreateRequestLogDto):
    async with AsyncSessionLocal() as session:
        await session.begin()
        await save_request_log(
            create_request_log_dto=create_request_log_dto,
            session=session,
        )
        await session.commit()
        await session.close()
