import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, func, text
from sqlalchemy.dialects.postgresql import TEXT, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models import Base


class VerificationType(Enum):
    EMAIL_VERIFICATION = "email_verification"
    PASSWORD_RESET = "password_reset"


class VerificationIdentifier:
    SEPARATOR = "::"

    @classmethod
    def build(cls, verification_type: VerificationType, target: str) -> str:
        return f"{verification_type.value}{cls.SEPARATOR}{target}"

    @classmethod
    def parse(cls, identifier: str) -> tuple[VerificationType, str]:
        if cls.SEPARATOR not in identifier:
            raise ValueError("Invalid identifier format")

        verification_type, target = identifier.split(cls.SEPARATOR, maxsplit=1)
        return VerificationType(verification_type), target


class Verification(Base):
    __tablename__ = "verifications"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    identifier: Mapped[str] = mapped_column(TEXT)
    value: Mapped[str] = mapped_column(TEXT)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
