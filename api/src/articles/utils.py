import tempfile

import aiohttp
import pymupdf
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


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
