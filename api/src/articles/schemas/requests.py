from pydantic import BaseModel, Field

from src.articles.models.note import Note


class ArticleCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    url: str = Field(..., min_length=1, max_length=255)
    page_numbers_to_delete: list[int] = Field(default=[])


class CreateArticleDto(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    url: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    notes: list[Note] = Field(...)


class ArticlesFindParams(BaseModel):
    name: str = Field("", max_length=255)
    url: str = Field("", max_length=255)
    offset: int = Field(0, ge=0)
    limit: int = Field(10, gt=0, le=50)
