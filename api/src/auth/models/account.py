import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, func, text
from sqlalchemy.dialects.postgresql import TEXT, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models import Base

if TYPE_CHECKING:
    from src.users.models.user import User


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    account_id: Mapped[str] = mapped_column(TEXT)
    provider_id: Mapped[str] = mapped_column(TEXT)
    access_token: Mapped[Optional[str]] = mapped_column(TEXT)
    refresh_token: Mapped[Optional[str]] = mapped_column(TEXT)
    id_token: Mapped[Optional[str]] = mapped_column(TEXT)
    password: Mapped[Optional[str]] = mapped_column(TEXT)
    scope: Mapped[Optional[str]] = mapped_column(TEXT)
    access_token_expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True)
    )
    refresh_token_expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
    )

    user: Mapped["User"] = relationship(
        back_populates="accounts",
    )
