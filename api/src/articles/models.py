import uuid
from datetime import datetime

from pydantic import BaseModel, Field
from sqlalchemy import DateTime, TypeDecorator, func, text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, TEXT, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models import Base


class Note(BaseModel):
    note: str = Field(..., description="The note extracted from the article.")
    page_numbers: list[int] = Field(
        ..., description="List of page numbers where the note is found."
    )

    def __repr__(self):
        return f"Note(note={self.note}, page_numbers={self.page_numbers})"


class NoteType(TypeDecorator):
    impl = JSONB

    def process_bind_param(self, value, dialect):
        if isinstance(value, Note):
            return value.model_dump()
        return value

    def process_result_value(self, value, dialect):
        if value:
            return Note(**value)
        return value


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
        ARRAY(NoteType),
        nullable=False,
    )
