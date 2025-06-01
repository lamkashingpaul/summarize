from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import TypeDecorator


class CustomJsonbType(TypeDecorator):
    impl = JSONB

    def __init__(self, model: type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model

    def process_bind_param(self, value, dialect):
        if isinstance(value, BaseModel):
            return value.model_dump()
        return value

    def process_result_value(self, value, dialect):
        if value:
            return self.model(**value)
        return value
