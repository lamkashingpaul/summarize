import uuid
from datetime import datetime

from sqlalchemy import DateTime, func, text
from sqlalchemy.dialects.postgresql import BOOLEAN, TEXT, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.auth.models.account import Account
from src.auth.models.session import Session
from src.database.models import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    name: Mapped[str] = mapped_column(
        TEXT,
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        TEXT,
        nullable=False,
        unique=True,
    )
    is_email_verified: Mapped[bool] = mapped_column(
        BOOLEAN,
        nullable=False,
    )
    image_url: Mapped[str] = mapped_column(
        TEXT,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    sessions: Mapped[list["Session"]] = relationship(
        back_populates="user",
        lazy="select",
    )
    accounts: Mapped[list["Account"]] = relationship(
        back_populates="user",
        lazy="select",
    )
