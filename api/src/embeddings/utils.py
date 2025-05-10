from langchain_core.documents import Document


def format_documents_to_string(documents: list[Document]) -> str:
    """
    Formats a list of Document objects into a string representation.
    Each document is represented by its page content and metadata.
    """
    return "\n\n".join(
        f"<<Content of Page {doc.metadata['page'] + 1}>>\n{doc.page_content}"
        for doc in documents
    )
