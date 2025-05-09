from langchain_cohere import CohereEmbeddings
from langchain_core.documents import Document

from src.database.service import SessionDep
from src.embeddings.models import Embedding
from src.embeddings.schemas import CreateEmbeddingDto


async def save_embeddings(
    documents: list[Document], url: str, session: SessionDep
) -> list[Embedding]:
    model = CohereEmbeddings(
        model="embed-english-v3.0",
        async_client=None,
        client=None,
    )

    embedded_documents = await model.aembed_documents(
        [doc.page_content for doc in documents]
    )

    embeddings = [
        Embedding(
            **CreateEmbeddingDto(
                content=document.page_content,
                embedding=embedded_document,
                additional_metadata={
                    **document.metadata,
                    "url": url,
                },
            ).model_dump()
        )
        for document, embedded_document in zip(documents, embedded_documents)
    ]

    session.add_all(embeddings)
    return embeddings
