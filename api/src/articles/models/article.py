import uuid
from datetime import datetime

from sqlalchemy import DateTime, func, text
from sqlalchemy.dialects.postgresql import ARRAY, TEXT, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.articles.models.note import Note, NoteType
from src.database.models import Base


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
