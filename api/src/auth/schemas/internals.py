from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from src.auth.models.verification import VerificationType
from src.users.models.user import User


class CreateVerificationDto(BaseModel):
    verification_type: VerificationType
    target: str
    expires_at: datetime


class CreateSessionDto(BaseModel):
    ip_address: Optional[str]
    user_agent: Optional[str]
    user: User

    model_config = ConfigDict(arbitrary_types_allowed=True)
