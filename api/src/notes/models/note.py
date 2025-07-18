import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, func, text
from sqlalchemy.dialects.postgresql import ARRAY, INTEGER, TEXT, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models import Base

if TYPE_CHECKING:
    from src.articles.models.article import Article


class Note(Base):
    __tablename__ = "notes"

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
    page_numbers: Mapped[list[int]] = mapped_column(ARRAY(INTEGER))
    article_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("articles.id"))

    article: Mapped["Article"] = relationship(back_populates="notes")
