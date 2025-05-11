from pydantic import BaseModel, Field
from sqlalchemy import TypeDecorator
from sqlalchemy.dialects.postgresql import JSONB


class Note(BaseModel):
    note: str = Field(..., description="The note extracted from the article.")
    page_numbers: list[int] = Field(
        ..., description="List of page numbers where the note is found."
    )

    def __repr__(self):
        return f"Note(note={self.note}, page_numbers={self.page_numbers})"


class NoteType(TypeDecorator):
    impl = JSONB

    def process_bind_param(self, value, dialect):
        if isinstance(value, Note):
            return value.model_dump()
        return value

    def process_result_value(self, value, dialect):
        if value:
            return Note(**value)
        return value
