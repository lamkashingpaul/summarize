from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ArticleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    url: str
    created_at: datetime


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
                    "created_at": "2023-10-01T12:00:00Z",
                }
            }
        }
    }


class GetArticlesResponse(BaseModel):
    articles_total_count: int
    articles_total_pages: int
    articles_has_next_page: bool
    articles: list[ArticleResponse]

    model_config = {
        "json_schema_extra": {
            "example": {
                "articles_total_count": 100,
                "articles_total_pages": 10,
                "articles_has_next_page": True,
                "articles": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "name": "Sample Article",
                        "url": "https://arxiv.org/pdf/sample.pdf",
                        "created_at": "2023-10-01T12:00:00Z",
                    }
                ],
            }
        }
    }
