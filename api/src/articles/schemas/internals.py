from dataclasses import dataclass
from typing import Sequence

from src.articles.models.article import Article


@dataclass
class FindArticlesReturn:
    articles_total_count: int
    articles_total_pages: int
    articles_has_next_page: bool
    articles: Sequence[Article]
