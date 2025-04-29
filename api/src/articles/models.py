from datetime import datetime
import uuid
from pydantic import BaseModel
from sqlalchemy import DateTime, func, text
from src.databases.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, TEXT, ARRAY, JSONB


class Note(BaseModel):
    note: str
    pageNumbers: list[int]


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    name: Mapped[str] = mapped_column(
        TEXT,
        nullable=False,
    )
    url: Mapped[str] = mapped_column(
        TEXT,
        nullable=False,
    )
    content: Mapped[str] = mapped_column(
        TEXT,
        nullable=False,
    )
    notes: Mapped[list[Note]] = mapped_column(
        ARRAY(JSONB),
        nullable=False,
    )
