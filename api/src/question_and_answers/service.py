from typing import cast

from langchain_cohere import CohereEmbeddings
from langchain_core.documents import Document
from langchain_deepseek import ChatDeepSeek

from src.articles.models.article import Article
from src.database.service import SessionDep
from src.embeddings.service import get_k_closest_embeddings
from src.embeddings.utils import format_documents_to_string
from src.errors.models import CustomDatabaseNotFoundException
from src.notes.models.note import Note
from src.prompts.service import generate_answer_prompt
from src.question_and_answers.schemas.internals import (
    GenerateAnswerChain,
    GenerateAnswerChainOutput,
    GenerateAnswerReturn,
)


async def get_article_documents_and_notes(
    article: Article, question: str, session: SessionDep
) -> tuple[list[Document], set[Note]]:
    notes = article.notes

    target_embedding = await CohereEmbeddings(
        model="embed-english-v3.0",
        async_client=None,
        client=None,
        request_timeout=10.0,
    ).aembed_query(question)

    embeddings = await get_k_closest_embeddings(
        target_embedding=target_embedding,
        article=article,
        k=5,
        session=session,
    )
    if not embeddings:
        raise CustomDatabaseNotFoundException(
            message="No embeddings found for the article.",
        )

    documents = [
        Document(
            page_content=embedding.content,
            metadata=embedding.additional_metadata,
        )
        for embedding in embeddings
    ]

    return documents, notes


async def answer_question(article: Article, question: str, session: SessionDep):
    documents, notes = await get_article_documents_and_notes(
        article=article,
        question=question,
        session=session,
    )

    response = await generate_answer(question, documents, notes)
    return response


async def generate_answer(
    question: str, documents: list[Document], notes: set[Note]
) -> GenerateAnswerReturn:
    documents_as_string = format_documents_to_string(documents)
    notes_as_string = "\n".join(note.content for note in notes)

    model = ChatDeepSeek(model="deepseek-chat", temperature=0.0)

    chain = cast(
        GenerateAnswerChain,
        generate_answer_prompt
        | model.with_structured_output(GenerateAnswerChainOutput),
    )

    response = await chain.ainvoke(
        {
            "documents": documents_as_string,
            "notes": notes_as_string,
            "question": question,
        }
    )

    return GenerateAnswerReturn(
        answer=response.answer,
        followup_questions=response.followup_questions,
        is_related=response.is_related,
    )
