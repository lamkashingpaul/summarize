from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.settings.service import settings

engine = create_async_engine(
    settings.database_url.encoded_string(),
    echo=settings.env == "development",
)

AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
