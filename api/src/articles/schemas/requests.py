from uuid import UUID

from fastapi import Path
from pydantic import BaseModel, Field, computed_field


class ArticleCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="The title of the article.",
    )
    url: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="The URL of the article.",
    )
    page_numbers_to_delete: list[int] = Field(
        default=[],
        description="List of page numbers to delete from the article.",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Sample Article",
                "url": "https://arxiv.org/pdf/sample.pdf",
                "page_numbers_to_delete": [1, 2],
            }
        }
    }


class ArticleGetParams(BaseModel):
    article_id: UUID = Path(
        ...,
        description="The ID of the article to retrieve.",
        example="123e4567-e89b-12d3-a456-426614174000",
    )


class ArticleUpdateParams(BaseModel):
    article_id: UUID = Path(
        ...,
        description="The ID of the article to update.",
        example="123e4567-e89b-12d3-a456-426614174000",
    )


class ArticlesFindQuery(BaseModel):
    title: str = Field(
        "",
        max_length=255,
        description="The title of the article to search for.",
    )
    url: str = Field(
        "",
        max_length=255,
        description="The URL of the article to search for.",
    )
    page_index: int = Field(
        0,
        ge=0,
        description="The index of the page to retrieve (0-based).",
    )
    page_size: int = Field(
        10,
        ge=1,
        le=50,
        description="The number of articles to retrieve per page.",
    )

    @computed_field
    @property
    def limit(self) -> int:
        return self.page_size

    @computed_field
    @property
    def offset(self) -> int:
        return self.page_index * self.page_size
