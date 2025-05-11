from pydantic import BaseModel, ConfigDict, Field


class QuestionAskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    answer: str = Field(...)
    followup_questions: list[str] = Field(...)
