from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ArticleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    url: str


class CreateArticleResponse(BaseModel):
    detail: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "Article created successfully.",
            }
        }
    }


class GetArticleByIdResponse(BaseModel):
    article: ArticleResponse

    model_config = {
        "json_schema_extra": {
            "example": {
                "article": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "name": "Sample Article",
                    "url": "https://arxiv.org/pdf/sample.pdf",
                }
            }
        }
    }


class GetArticlesResponse(BaseModel):
    articles: list[ArticleResponse]

    model_config = {
        "json_schema_extra": {
            "example": {
                "articles": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "name": "Sample Article",
                        "url": "https://arxiv.org/pdf/sample.pdf",
                    }
                ]
            }
        }
    }
