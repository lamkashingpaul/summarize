from datetime import datetime

from pydantic import BaseModel

from src.auth.models.verification import VerificationType


class CreateVerificationDto(BaseModel):
    verification_type: VerificationType
    target: str
    expires_at: datetime
