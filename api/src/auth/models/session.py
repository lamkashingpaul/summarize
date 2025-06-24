import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, func, text
from sqlalchemy.dialects.postgresql import TEXT, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models import Base

if TYPE_CHECKING:
    from src.users.models.user import User


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    token: Mapped[str] = mapped_column(TEXT, unique=True)
    ip_address: Mapped[Optional[str]] = mapped_column(TEXT)
    user_agent: Mapped[Optional[str]] = mapped_column(TEXT)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(back_populates="sessions")
