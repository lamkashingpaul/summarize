from pydantic import BaseModel, Field


class QuestionAsk(BaseModel):
    url: str = Field(..., min_length=1, max_length=255)
    question: str = Field(..., min_length=1, max_length=255)


class QuestionAskResponse(BaseModel):
    answer: str = Field(...)
    followup_questions: list[str] = Field(...)
