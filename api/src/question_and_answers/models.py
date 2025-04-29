from src.databases.base import Base
from sqlalchemy import DateTime, func, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, TEXT, ARRAY
import uuid
from datetime import datetime


class QuestionAndAnswer(Base):
    __tablename__ = "question_and_answers"

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
    context: Mapped[str] = mapped_column(
        TEXT,
        nullable=False,
    )
    question: Mapped[str] = mapped_column(
        TEXT,
        nullable=False,
    )
    answer: Mapped[str] = mapped_column(
        TEXT,
        nullable=False,
    )
    followup_questions: Mapped[list[str]] = mapped_column(
        ARRAY(TEXT),
        nullable=False,
    )
