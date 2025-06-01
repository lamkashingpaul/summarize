from pydantic import BaseModel, ConfigDict

from src.articles.models.article import Article


class CreateEmbeddingDto(BaseModel):
    content: str
    embedding: list[float]
    additional_metadata: dict
    article: Article

    model_config = ConfigDict(arbitrary_types_allowed=True)


CreateEmbeddingDto.model_rebuild()
