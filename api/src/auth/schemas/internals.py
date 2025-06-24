from datetime import datetime

from pydantic import BaseModel


class CreateVerificationDto(BaseModel):
    identifier: str
    expires_at: datetime
