import uuid
from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, func, text
from sqlalchemy.dialects.postgresql import JSONB, TEXT, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models import Base


class Embedding(Base):
    __tablename__ = "embeddings"

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
    content: Mapped[str] = mapped_column(
        TEXT,
        nullable=False,
    )
    embedding: Mapped[list[float]] = mapped_column(
        Vector,
        nullable=False,
    )
    additional_metadata: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )
