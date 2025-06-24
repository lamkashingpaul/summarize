from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ArticleResponse(BaseModel):
    id: UUID
    title: str
    url: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Sample Article",
                "url": "https://arxiv.org/pdf/sample.pdf",
                "created_at": "2023-10-01T12:00:00Z",
            }
        },
    )


class CreateArticleResponse(BaseModel):
    detail: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detail": "Article created successfully.",
            }
        }
    )


class GetArticleByIdResponse(BaseModel):
    article: ArticleResponse

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "article": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "title": "Sample Article",
                    "url": "https://arxiv.org/pdf/sample.pdf",
                    "created_at": "2023-10-01T12:00:00Z",
                }
            }
        }
    )


class UpdateArticleByIdResponse(BaseModel):
    article: ArticleResponse

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "article": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "title": "Updated Sample Article",
                    "url": "https://arxiv.org/pdf/sample_updated.pdf",
                    "created_at": "2023-10-01T12:00:00Z",
                }
            }
        }
    )


class SearchArticlesResponse(BaseModel):
    articles_total_count: int
    articles_total_pages: int
    articles_has_next_page: bool
    articles: list[ArticleResponse]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "articles_total_count": 100,
                "articles_total_pages": 10,
                "articles_has_next_page": True,
                "articles": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "title": "Sample Article",
                        "url": "https://arxiv.org/pdf/sample.pdf",
                        "created_at": "2023-10-01T12:00:00Z",
                    }
                ],
            }
        }
    )
