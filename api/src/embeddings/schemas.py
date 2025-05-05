from pydantic import BaseModel


class CreateEmbeddingDto(BaseModel):
    content: str
    embedding: list[float]
    additional_metadata: dict
