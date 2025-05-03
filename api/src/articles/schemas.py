from pydantic import BaseModel, Field


class ArticleCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    url: str = Field(..., min_length=1, max_length=255)
    page_numbers_to_delete: list[int] = Field(default=[])
