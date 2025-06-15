import uuid
from datetime import datetime

from sqlalchemy import DateTime, func, text
from sqlalchemy.dialects.postgresql import INTEGER, JSONB, REAL, TEXT, UUID, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models import Base


class RequestLog(Base):
    __tablename__ = "request_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        index=True,
    )
    client_ip: Mapped[str] = mapped_column(
        VARCHAR(45),
        nullable=False,
        index=True,
    )
    method: Mapped[str] = mapped_column(
        VARCHAR(10),
        nullable=False,
    )
    path: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False,
        index=True,
    )
    query_params: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )
    request_header: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )
    request_body: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )
    response_status: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False,
    )
    response_header: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )
    response_body: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )
    duration_ms: Mapped[float] = mapped_column(
        REAL,
        nullable=False,
    )
    error: Mapped[str] = mapped_column(TEXT, nullable=False)
