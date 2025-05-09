from langchain_cohere import CohereEmbeddings
from langchain_core.documents import Document
from langchain_deepseek import ChatDeepSeek
from sqlalchemy import select

from src.articles.models import Note
from src.database.service import SessionDep
from src.embeddings.models import Embedding
from src.errors.models import CustomDatabaseNotFoundException
from src.prompts.service import (
    answer_question_prompt,
    format_answer_to_question,
    format_output_answer_to_question,
)


async def answer_question(
    url: str, question: str, notes: list[Note], session: SessionDep
) -> tuple[str, list[str]]:
    model = CohereEmbeddings(
        model="embed-english-v3.0",
        async_client=None,
        client=None,
        request_timeout=10.0,
    )
    target_embedding = await model.aembed_query(question)

    statement = (
        select(Embedding)
        .where(Embedding.additional_metadata.comparator.contains({"url": url}))
        .order_by(Embedding.embedding.l2_distance(target_embedding))
        .limit(5)
    )
    embeddings = (await session.scalars(statement)).all()
    if not embeddings:
        raise CustomDatabaseNotFoundException(
            message="No embeddings found for the given URL."
        )

    documents = [
        Document(page_content=embedding.content, metadata=embedding.additional_metadata)
        for embedding in embeddings
    ]

    answer, followup_questions = await generate_answer(question, documents, notes)
    return answer, followup_questions


async def generate_answer(
    question: str, documents: list[Document], notes: list[Note]
) -> tuple[str, list[str]]:
    documents_as_string = "\n\n".join(
        f"<<Content of Page {doc.metadata['page'] + 1}>>\n{doc.page_content}"
        for doc in documents
    )
    notes_as_string = "\n".join(note.note for note in notes)

    model = ChatDeepSeek(model="deepseek-chat", temperature=0.0)

    model_with_tools = model.bind_tools(
        tools=[format_answer_to_question], tool_choice="any"
    )

    chain = answer_question_prompt | model_with_tools | format_output_answer_to_question

    response = await chain.ainvoke(
        {
            "documents": documents_as_string,
            "notes": notes_as_string,
            "question": question,
        }
    )

    answer, followup_questions = response

    return answer, followup_questions
