import uuid
from datetime import datetime

from sqlalchemy import DateTime, func, text
from sqlalchemy.dialects.postgresql import TEXT, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models import Base
from src.embeddings.models.embedding import Embedding
from src.notes.models.note import Note


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
    title: Mapped[str] = mapped_column(
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

    notes: Mapped[list["Note"]] = relationship(
        back_populates="article",
        lazy="select",
    )
    embeddings: Mapped[list["Embedding"]] = relationship(
        back_populates="article",
        lazy="select",
    )
