from typing import Literal, Optional, overload
from uuid import UUID

from sqlalchemy import func, select

from src.articles.models.article import Article
from src.articles.schemas.internals import CreateArticleDto, FindArticlesReturn
from src.articles.schemas.requests import ArticlesFindQuery
from src.database.service import SessionDep
from src.errors.models import CustomDatabaseNotFoundException


async def save_article(create_article_dto: CreateArticleDto, session: SessionDep):
    article = Article(**create_article_dto.model_dump())
    session.add(article)
    return article


@overload
async def fetch_article_by_id(
    article_id: UUID, session: SessionDep, should_fail: Literal[True]
) -> Article: ...
@overload
async def fetch_article_by_id(
    article_id: UUID, session: SessionDep, should_fail: Literal[False] = False
) -> Optional[Article]: ...
async def fetch_article_by_id(
    article_id: UUID, session: SessionDep, should_fail: bool = False
) -> Optional[Article]:
    statement = select(Article).where(Article.id == article_id).limit(2)
    articles = (await session.scalars(statement)).all()

    if len(articles) != 1:
        if should_fail:
            raise CustomDatabaseNotFoundException(
                message=f"Article with id: {article_id} not found."
            )
        return None

    return articles[0]


@overload
async def fetch_article_by_url(
    url: str, session: SessionDep, should_fail: Literal[True]
) -> Article: ...
@overload
async def fetch_article_by_url(
    url: str, session: SessionDep, should_fail: Literal[False] = False
) -> Optional[Article]: ...
async def fetch_article_by_url(
    url: str, session: SessionDep, should_fail: bool = False
) -> Optional[Article]:
    statement = select(Article).where(Article.url == url).limit(2)
    articles = (await session.scalars(statement)).all()

    if len(articles) != 1:
        if should_fail:
            raise CustomDatabaseNotFoundException(
                message=f"Article with url: {url} not found."
            )
        return None

    return articles[0]


async def find_articles(
    query: ArticlesFindQuery, session: SessionDep
) -> FindArticlesReturn:
    title = query.title
    url = query.url
    page_index = query.page_index
    offset = query.offset
    limit = query.limit

    filters = []
    if title:
        filters.append(Article.title.ilike(f"%{title}%"))
    if url:
        filters.append(Article.url.ilike(f"%{url}%"))

    data_statement = (
        select(Article)
        .where(*filters)
        .order_by(Article.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    count_statement = select(func.count()).select_from(Article).where(*filters)

    articles = (await session.scalars(data_statement)).all()
    total_count = await session.scalar(count_statement) or 0
    corrected_limit = limit or total_count or 1
    total_pages = (total_count + corrected_limit - 1) // corrected_limit
    has_next_page = page_index + 1 < total_pages

    return FindArticlesReturn(
        articles_total_count=total_count,
        articles_total_pages=total_pages,
        articles_has_next_page=has_next_page,
        articles=articles,
    )
