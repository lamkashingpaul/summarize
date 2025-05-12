import asyncio
from typing import Annotated

from fastapi import APIRouter, Path, Query

from src.articles.schemas.requests import (
    ArticleCreate,
    ArticleGetParams,
    ArticlesFindQuery,
    CreateArticleDto,
)
from src.articles.schemas.responses import (
    ArticleResponse,
    CreateArticleResponse,
    GetArticleByIdResponse,
    GetArticlesResponse,
)
from src.articles.service import (
    convert_pdf_to_documents,
    delete_page_numbers_from_pdf,
    download_article,
    fetch_article_by_id_or_fail,
    fetch_article_by_url_or_fail,
    find_articles,
    generate_notes,
    save_article,
)
from src.database.service import SessionDep
from src.embeddings.service import save_embeddings
from src.error_handlers.decorators import custom_exception_handler_for_http
from src.errors.models import CustomHttpException

articles_router = APIRouter(prefix="/articles", tags=["articles"])


@articles_router.post("", status_code=201)
@custom_exception_handler_for_http
async def create_article(
    article: ArticleCreate,
    session: SessionDep,
) -> CreateArticleResponse:
    name = article.name
    url = article.url
    page_numbers_to_delete = article.page_numbers_to_delete

    if not url.startswith("https://arxiv.org/pdf/"):
        raise CustomHttpException(
            status_code=400,
            detail="Invalid URL. Only arXiv PDF URLs are supported.",
        )

    existing_articles = await fetch_article_by_url_or_fail(url=url, session=session)
    if existing_articles:
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

    notes = await generate_notes(documents)

    save_article_task = save_article(
        create_article_dto=CreateArticleDto(
            name=name,
            url=url,
            content="\n".join(doc.page_content for doc in documents),
            notes=notes,
        ),
        session=session,
    )
    save_embeddings_task = save_embeddings(
        documents=documents, url=url, session=session
    )

    await asyncio.gather(save_article_task, save_embeddings_task)

    await session.commit()
    return CreateArticleResponse(detail="Article created successfully.")


@articles_router.get("/{article_id}")
@custom_exception_handler_for_http
async def get_article_by_id(
    params: Annotated[ArticleGetParams, Path()],
    session: SessionDep,
) -> GetArticleByIdResponse:
    article_id = params.article_id
    article = await fetch_article_by_id_or_fail(article_id=article_id, session=session)
    return GetArticleByIdResponse(
        article=ArticleResponse.model_construct(**article.__dict__)
    )


@articles_router.get("")
@custom_exception_handler_for_http
async def get_articles(
    query: Annotated[ArticlesFindQuery, Query()],
    session: SessionDep,
) -> GetArticlesResponse:
    articles = await find_articles(query=query, session=session)
    return GetArticlesResponse.model_construct(
        articles=[
            ArticleResponse.model_construct(**article.__dict__) for article in articles
        ]
    )
