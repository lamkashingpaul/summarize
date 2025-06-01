from pydantic import BaseModel


class AskQuestionResponse(BaseModel):
    answer: str
    followup_questions: list[str]
    is_related: bool

    model_config = {
        "json_schema_extra": {
            "example": {
                "answer": "The answer to the question.",
                "followup_questions": [
                    "What is the main topic?",
                    "Can you explain further?",
                ],
                "is_related": True,
            }
        }
    }
