from langchain_cohere import CohereEmbeddings
from langchain_core.documents import Document
from sqlalchemy import select

from src.articles.models import Note
from src.database.service import SessionDep
from src.embeddings.models import Embedding


async def answer_question(
    url: str, question: str, notes: list[Note], session: SessionDep
) -> tuple[str, list[str]]:
    model = CohereEmbeddings(model="embed-english-v3.0", async_client=None, client=None)
    embedding = model.embed_query(question)

    statement = (
        select(Embedding.content, Embedding.additional_metadata)
        .where(Embedding.additional_metadata.comparator.contains({"url": url}))
        .order_by(Embedding.embedding.l2_distance(embedding))
        .limit(5)
    )
    embeddings = (await session.scalars(statement)).all()
    if not embeddings:
        raise ValueError("No embeddings found in the database.")

    print(embeddings)

    documents = [
        Document(page_content=content, metadata=additional_metadata)
        for (content, additional_metadata) in embeddings
    ]

    answer, followup_questions = await generate_answer(question, documents, notes)
    return answer, followup_questions


async def generate_answer(
    question: str, documents: list[Document], notes: list[Note]
) -> tuple[str, list[str]]:
    # Placeholder for the actual answer generation logic
    # This should be replaced with the actual implementation
    answer = "This is a placeholder answer."
    followup_questions = ["What do you think about this?"]

    return answer, followup_questions
