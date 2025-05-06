from typing import Annotated

from fastapi import APIRouter, HTTPException, Query

from src.articles.schemas import (
    ArticleCreate,
    ArticlesFindParams,
    CreateArticleDto,
    CreateArticleResponse,
)
from src.articles.service import (
    convert_pdf_to_documents,
    delete_page_numbers_from_pdf,
    download_article,
    fetch_article_or_fail,
    find_articles,
    generate_notes,
    save_article,
)
from src.database.service import SessionDep
from src.embeddings.service import save_embeddings

articles_router = APIRouter(prefix="/articles", tags=["articles"])


@articles_router.post("")
async def create_article(
    article: ArticleCreate, session: SessionDep
) -> CreateArticleResponse:
    name = article.name
    url = article.url
    page_numbers_to_delete = article.page_numbers_to_delete

    if not url.startswith("https://arxiv.org/pdf/"):
        raise HTTPException(
            status_code=400,
            detail={"message": "Invalid URL. Only arXiv PDF URLs are supported."},
        )

    find_articles_query = ArticlesFindParams(url=url, offset=0, limit=1)
    existing_articles = await find_articles(query=find_articles_query, session=session)
    if existing_articles:
        raise HTTPException(
            status_code=400,
            detail={"message": "Article already exists."},
        )

    downloaded_article = await download_article(url)
    if page_numbers_to_delete:
        downloaded_article = delete_page_numbers_from_pdf(
            downloaded_article, page_numbers_to_delete
        )

    documents = convert_pdf_to_documents(downloaded_article)

    notes = await generate_notes(documents)

    save_article(
        create_article_dto=CreateArticleDto(
            name=name,
            url=url,
            content="\n".join(doc.page_content for doc in documents),
            notes=notes,
        ),
        session=session,
    )
    save_embeddings(documents=documents, url=url, session=session)
    await session.commit()

    return CreateArticleResponse(notes=notes)


@articles_router.get("/{article_id}")
async def get_article_by_id(article_id: str, session: SessionDep):
    article = await fetch_article_or_fail(article_id=article_id, session=session)
    return {"article": article}


@articles_router.get("")
async def get_articles(
    query: Annotated[ArticlesFindParams, Query()],
    session: SessionDep,
):
    articles = await find_articles(query=query, session=session)
    return {"articles": articles}
