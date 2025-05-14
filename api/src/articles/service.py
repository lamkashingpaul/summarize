import tempfile
from uuid import UUID

import aiohttp
import pymupdf
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document
from langchain_deepseek import ChatDeepSeek
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sqlalchemy import func, select
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.articles.models.article import Article
from src.articles.models.note import Note
from src.articles.schemas.internals import FindArticlesReturn
from src.articles.schemas.requests import ArticlesFindQuery, CreateArticleDto
from src.database.service import SessionDep
from src.embeddings.utils import format_documents_to_string
from src.errors.models import CustomDatabaseNotFoundException
from src.prompts.service import format_note, format_output_notes, notes_prompt


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

    loader = PyMuPDFLoader(temp_file_path)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""],
    )
    documents = []

    for document in loader.lazy_load():
        cleaned_content = " ".join(
            line for line in map(str.strip, document.page_content.split("\n")) if line
        ).replace("  ", " ")

        document.page_content = cleaned_content.replace(
            ". ",
            ".\n\n",
        ).replace(
            "\u0000",
            "",
        )
        chunks = text_splitter.split_documents([document])
        for chunk in chunks:
            chunk.metadata["page"] = document.metadata["page"]
            documents.append(chunk)

    return documents


async def generate_notes(documents: list[Document]) -> list[Note]:
    documents_as_string = format_documents_to_string(documents)
    model = ChatDeepSeek(model="deepseek-chat", temperature=0.0)

    model_with_tools = model.bind_tools(tools=[format_note], tool_choice="any")

    chain = notes_prompt | model_with_tools | format_output_notes

    response = await chain.ainvoke({"article": documents_as_string})

    return response


async def save_article(create_article_dto: CreateArticleDto, session: SessionDep):
    article = Article(**create_article_dto.model_dump())
    session.add(article)
    return article


async def fetch_article_by_id_or_fail(
    article_id: UUID, session: AsyncSession
) -> Article:
    try:
        statement = select(Article).where(Article.id == article_id).limit(2)
        article = (await session.scalars(statement)).one()
        return article

    except (NoResultFound, MultipleResultsFound) as e:
        raise CustomDatabaseNotFoundException(
            message=f"Article with id: {article_id} not found"
        ) from e


async def fetch_article_by_url(url: str, session: AsyncSession):
    statement = select(Article).where(Article.url == url).limit(2)
    article = (await session.scalars(statement)).one_or_none()
    return article


async def find_articles(
    query: ArticlesFindQuery, session: SessionDep
) -> FindArticlesReturn:
    name = query.name
    url = query.url
    page_index = query.page_index
    offset = query.offset
    limit = query.limit

    filters = []
    if name:
        filters.append(Article.name.ilike(f"%{name}%"))
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
