from typing import Sequence

from langchain_cohere import CohereEmbeddings
from langchain_core.documents import Document
from sqlalchemy import select

from src.articles.models.article import Article
from src.database.service import SessionDep
from src.embeddings.models.embedding import Embedding
from src.embeddings.schemas.internals import CreateEmbeddingDto


async def get_k_closest_embeddings(
    target_embedding: list[float],
    article: Article,
    k: int,
    session: SessionDep,
) -> Sequence[Embedding]:
    statement = (
        select(Embedding)
        .where(Embedding.article == article)
        .order_by(Embedding.embedding.l2_distance(target_embedding))
        .limit(k)
    )
    embeddings = (await session.scalars(statement)).all()
    return embeddings


async def save_embeddings(
    documents: list[Document], article: Article, session: SessionDep
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
                additional_metadata=document.metadata,
                article=article,
            ).model_dump()
        )
        for document, embedded_document in zip(documents, embedded_documents)
    ]

    session.add_all(embeddings)
    return embeddings
