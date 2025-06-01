from dataclasses import dataclass
from typing import Sequence

from pydantic import BaseModel, Field

from src.articles.models.article import Article


class CreateArticleDto(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    url: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)


@dataclass
class FindArticlesReturn:
    articles_total_count: int
    articles_total_pages: int
    articles_has_next_page: bool
    articles: Sequence[Article]
