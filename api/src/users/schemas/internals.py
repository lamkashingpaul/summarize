from typing import Optional

from pydantic import BaseModel


class CreateUserDto(BaseModel):
    email: str
    password: str
    name: str
    image_url: Optional[str] = None
