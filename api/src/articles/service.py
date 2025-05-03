import tempfile
import aiohttp
from langchain_cohere import ChatCohere
from langchain_cohere import ChatCohere
import pymupdf
from src.prompts.service import format_notes, format_output, notes_prompt
from langchain_core.documents import Document
from src.articles.models import Note
from langchain_unstructured import UnstructuredLoader
from src.settings.service import settings


async def download_article(url: str) -> bytes:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.read()


async def delete_page_numbers_from_pdf(
    pdf_data: bytes, page_numbers_to_delete: list[int]
) -> bytes:
    pdf_document = pymupdf.open(stream=pdf_data, filetype="pdf")
    for page_number in sorted(set(page_numbers_to_delete), reverse=True):
        pdf_document.delete_page(page_number - 1)

    modified_pdf_data = pdf_document.write()
    pdf_document.close()

    return modified_pdf_data


async def convert_pdf_to_documents(pdf_data: bytes) -> list[Document]:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(pdf_data)
        temp_file_path = temp_file.name

    loader = UnstructuredLoader(
        file_path=temp_file_path,
        strategy="hi_res",
        partition_via_api=True,
    )

    documents: list[Document] = []
    for doc in loader.lazy_load():
        documents.append(doc)

    return documents


async def generate_notes(documents: list[Document]) -> list[Note]:
    documentsAsString = "\n".join(doc.page_content for doc in documents)
    model = ChatCohere(
        model="command-r",
        temperature=0,
    )

    model_with_tools = model.bind_tools(
        tools=[format_notes],
        tool_choice="required",
    )

    chain = notes_prompt | model_with_tools | format_output

    response = chain.invoke({"article": documentsAsString})

    return response
