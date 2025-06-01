from typing import Annotated

from fastapi import APIRouter, Path, Request

from src.articles.service import fetch_article_by_id
from src.database.service import SessionDep
from src.error_handlers.decorators import custom_exception_handler_for_http
from src.question_and_answers.schemas.requests import QuestionAsk, QuestionAskParams
from src.question_and_answers.schemas.responses import AskQuestionResponse
from src.question_and_answers.service import answer_question
from src.rate_limiter.service import limiter

question_and_answers_router = APIRouter(
    prefix="/question-and-answers", tags=["question and answers"]
)


@question_and_answers_router.post("/articles/{article_id}/questions")
@limiter.limit("5/minute")
@custom_exception_handler_for_http
async def ask_question(
    request: Request,
    params: Annotated[QuestionAskParams, Path()],
    question_ask: QuestionAsk,
    session: SessionDep,
) -> AskQuestionResponse:
    article_id = params.article_id
    article = await fetch_article_by_id(
        article_id=article_id, session=session, should_fail=True
    )

    question = question_ask.question
    response = await answer_question(
        article=article, question=question, session=session
    )

    return AskQuestionResponse(
        answer=response.answer,
        followup_questions=response.followup_questions,
        is_related=response.is_related,
    )
