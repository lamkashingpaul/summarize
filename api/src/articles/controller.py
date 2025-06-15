import asyncio
from typing import Annotated

from fastapi import APIRouter, Path, Query

from src.articles.schemas.internals import CreateArticleDto
from src.articles.schemas.requests import (
    ArticleCreate,
    ArticleGetParams,
    ArticlesFindQuery,
)
from src.articles.schemas.responses import (
    ArticleResponse,
    CreateArticleResponse,
    GetArticleByIdResponse,
    SearchArticlesResponse,
)
from src.articles.service import (
    fetch_article_by_id,
    fetch_article_by_url,
    find_articles,
    save_article,
)
from src.articles.utils import (
    convert_pdf_to_documents,
    delete_page_numbers_from_pdf,
    download_article,
)
from src.database.service import SessionDep
from src.embeddings.service import save_embeddings
from src.error_handlers.decorators import custom_exception_handler_for_http
from src.errors.models import CustomHttpException
from src.notes.service import save_notes
from src.utils.custom_api_route import CustomAPIRoute
from src.utils.temporary_disable import temporary_disable

articles_router = APIRouter(
    prefix="/articles",
    tags=["articles"],
    route_class=CustomAPIRoute,
)


@articles_router.post("", status_code=201)
@temporary_disable
@custom_exception_handler_for_http
async def create_article(
    article_create: ArticleCreate,
    session: SessionDep,
) -> CreateArticleResponse:
    title = article_create.title
    url = article_create.url
    page_numbers_to_delete = article_create.page_numbers_to_delete

    if not url.startswith("https://arxiv.org/pdf/"):
        raise CustomHttpException(
            status_code=400,
            detail="Invalid URL. Only arXiv PDF URLs are supported.",
        )

    existing_articles = await fetch_article_by_url(url=url, session=session)
    if existing_articles is not None:
        raise CustomHttpException(
            status_code=400,
            detail="Article already exists.",
        )

    downloaded_article = await download_article(url)
    if page_numbers_to_delete:
        downloaded_article = delete_page_numbers_from_pdf(
            downloaded_article, page_numbers_to_delete
        )

    documents = convert_pdf_to_documents(downloaded_article)

    article = await save_article(
        create_article_dto=CreateArticleDto(
            title=title,
            url=url,
            content="\n".join(doc.page_content for doc in documents),
        ),
        session=session,
    )

    save_embeddings_task = save_embeddings(
        documents=documents,
        article=article,
        session=session,
    )
    save_notes_task = save_notes(
        documents=documents,
        article=article,
        session=session,
    )
    await asyncio.gather(save_embeddings_task, save_notes_task)

    await session.commit()
    return CreateArticleResponse(detail="Article created successfully.")


@articles_router.get("/search")
@custom_exception_handler_for_http
async def search_articles(
    query: Annotated[ArticlesFindQuery, Query()],
    session: SessionDep,
) -> SearchArticlesResponse:
    res = await find_articles(query=query, session=session)

    return SearchArticlesResponse.model_construct(
        articles_total_count=res.articles_total_count,
        articles_total_pages=res.articles_total_pages,
        articles_has_next_page=res.articles_has_next_page,
        articles=list(
            map(
                lambda article: ArticleResponse.model_construct(**article.__dict__),
                res.articles,
            )
        ),
    )


@articles_router.get("/{article_id}")
@custom_exception_handler_for_http
async def get_article_by_id(
    params: Annotated[ArticleGetParams, Path()],
    session: SessionDep,
) -> GetArticleByIdResponse:
    article_id = params.article_id
    article = await fetch_article_by_id(
        article_id=article_id,
        session=session,
        should_fail=True,
    )

    return GetArticleByIdResponse(
        article=ArticleResponse.model_construct(**article.__dict__)
    )
