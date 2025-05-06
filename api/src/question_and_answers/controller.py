from fastapi import APIRouter, HTTPException

from src.articles.schemas import ArticlesFindParams
from src.articles.service import find_articles
from src.database.service import SessionDep
from src.question_and_answers.schemas import QuestionAsk, QuestionAskResponse
from src.question_and_answers.service import answer_question

question_and_answers_router = APIRouter(
    prefix="/question-and-answers", tags=["question-and-answers"]
)


@question_and_answers_router.post("/ask")
async def ask_question(
    question_ask: QuestionAsk, session: SessionDep
) -> QuestionAskResponse:
    find_articles_query = ArticlesFindParams(url=question_ask.url, offset=0, limit=1)
    existing_articles = await find_articles(query=find_articles_query, session=session)
    if not existing_articles:
        raise HTTPException(
            status_code=400,
            detail={"message": "Article does not exist."},
        )
    notes = existing_articles[0].notes

    answer, followup_questions = await answer_question(
        url=question_ask.url,
        question=question_ask.question,
        notes=notes,
        session=session,
    )

    return QuestionAskResponse(
        answer=answer,
        followup_questions=followup_questions,
    )
