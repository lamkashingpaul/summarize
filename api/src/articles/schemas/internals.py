from dataclasses import dataclass
from typing import Sequence

from pydantic import BaseModel

from src.articles.models.article import Article


class CreateArticleDto(BaseModel):
    title: str
    url: str
    content: str


@dataclass
class FindArticlesReturn:
    articles_total_count: int
    articles_total_pages: int
    articles_has_next_page: bool
    articles: Sequence[Article]
