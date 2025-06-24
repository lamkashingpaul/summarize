import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, ForeignKey, func, text
from sqlalchemy.dialects.postgresql import JSONB, TEXT, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models import Base

if TYPE_CHECKING:
    from src.articles.models.article import Article


class Embedding(Base):
    __tablename__ = "embeddings"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    content: Mapped[str] = mapped_column(TEXT)
    embedding: Mapped[list[float]] = mapped_column(Vector)
    additional_metadata: Mapped[dict] = mapped_column(JSONB)
    article_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("articles.id"))

    article: Mapped["Article"] = relationship(back_populates="embeddings")
