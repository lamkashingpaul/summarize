from fastapi import APIRouter, HTTPException
from src.articles.schemas import ArticleCreate
from src.articles.service import (
    convert_pdf_to_documents,
    delete_page_numbers_from_pdf,
    download_article,
    generate_notes,
)

articles_router = APIRouter(prefix="/articles", tags=["articles"])


@articles_router.post("")
async def create_article(article: ArticleCreate):
    name = article.name
    url = article.url
    page_numbers_to_delete = article.page_numbers_to_delete

    if not url.startswith("https://arxiv.org/pdf/"):
        raise HTTPException(
            status_code=400,
            detail={"message": "Invalid URL. Only arXiv PDF URLs are supported."},
        )

    downloaded_article = await download_article(url)

    if page_numbers_to_delete:
        downloaded_article = await delete_page_numbers_from_pdf(
            downloaded_article, page_numbers_to_delete
        )

    documents = await convert_pdf_to_documents(downloaded_article)

    notes = await generate_notes(documents)

    return {
        "notes": notes,
    }
