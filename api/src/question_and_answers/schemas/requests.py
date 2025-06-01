from uuid import UUID

from fastapi import Path
from pydantic import BaseModel, Field


class QuestionAskParams(BaseModel):
    article_id: UUID = Path(
        ...,
        description="The ID of the article to ask a question about.",
        example="123e4567-e89b-12d3-a456-426614174000",
    )


class QuestionAsk(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="The question to ask about the article.",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "question": "What are the main findings of this article?",
            }
        }
    }
