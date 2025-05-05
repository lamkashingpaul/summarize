from langchain_cohere import CohereEmbeddings
from langchain_core.documents import Document

from src.database.service import SessionDep
from src.embeddings.models import Embedding
from src.embeddings.schemas import CreateEmbeddingDto


def save_embeddings(
    documents: list[Document], url: str, session: SessionDep
) -> list[Embedding]:
    model = CohereEmbeddings(
        model="embed-english-v3.0",
        async_client=None,
        client=None,
    )

    embedded_documents = model.embed_documents([doc.page_content for doc in documents])

    embeddings = [
        Embedding(
            **CreateEmbeddingDto(
                content=documents[i].page_content,
                embedding=embedded_documents[i],
                additional_metadata={
                    **documents[i].metadata,
                    "url": url,
                },
            ).model_dump()
        )
        for i in range(len(embedded_documents))
    ]

    session.add_all(embeddings)
    return embeddings
