from pydantic import field_validator
from pydantic_settings import BaseSettings


class CustomBaseSettings(BaseSettings):
    @field_validator("*", mode="before")
    @classmethod
    def empty_string_to_none(cls, value):
        if isinstance(value, str) and value.strip() == "":
            return None
        return value
