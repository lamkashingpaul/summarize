import tempfile

import aiohttp
import pymupdf
from langchain_core.documents import Document
from langchain_deepseek import ChatDeepSeek
from langchain_unstructured import UnstructuredLoader
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.articles.models import Article, Note
from src.articles.schemas import CreateArticleDto
from src.database.service import SessionDep
from src.prompts.service import format_note, format_output, notes_prompt


async def download_article(url: str) -> bytes:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.read()


def delete_page_numbers_from_pdf(
    pdf_data: bytes, page_numbers_to_delete: list[int]
) -> bytes:
    pdf_document = pymupdf.open(stream=pdf_data, filetype="pdf")
    for page_number in sorted(set(page_numbers_to_delete), reverse=True):
        pdf_document.delete_page(page_number - 1)

    modified_pdf_data = pdf_document.write()
    pdf_document.close()

    return modified_pdf_data


def convert_pdf_to_documents(pdf_data: bytes) -> list[Document]:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(pdf_data)
        temp_file_path = temp_file.name

    loader = UnstructuredLoader(
        file_path=temp_file_path,
        strategy="hi_res",
        partition_via_api=True,
    )

    documents = [doc for doc in loader.lazy_load()]
    return documents


async def generate_notes(documents: list[Document]) -> list[Note]:
    documentsAsString = "\n".join(doc.page_content for doc in documents)
    model = ChatDeepSeek(
        model="deepseek-chat",
        temperature=0.0,
    )

    model_with_tools = model.bind_tools(
        tools=[format_note],
        tool_choice="any",
    )

    chain = notes_prompt | model_with_tools | format_output

    response = await chain.ainvoke({"article": documentsAsString})

    return response


def save_article(create_article_dto: CreateArticleDto, session: SessionDep):
    article = Article(**create_article_dto.model_dump())
    session.add(article)
    return article


async def fetch_article(article_id: str, session: AsyncSession) -> Article:
    statement = select(Article).where(Article.id == article_id).limit(2)
    article = (await session.scalars(statement)).one()
    return article
