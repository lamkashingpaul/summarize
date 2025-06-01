from dataclasses import dataclass
from typing import Annotated, Generic, Literal, TypedDict, TypeVar, Union

from langchain_core.runnables import Runnable
from pydantic import BaseModel, ConfigDict, Field

EventType = TypeVar("EventType", bound=str)
EventData = TypeVar("EventData")


class GenerateAnswerChainInput(TypedDict):
    documents: Annotated[str, ..., "Documents that are relevant to the question"]
    notes: Annotated[str, ..., "Notes that are relevant to the question"]
    question: Annotated[str, ..., "Question to ask"]


class GenerateAnswerChainOutput(BaseModel):
    """
    GenerateAnswerChainOutput schema for the response of a question-asking operation.
    This schema includes the answer to the question, follow-up questions, and
    whether the question is related to the provided context.
    Attributes:
        answer (str): Full textual response to the question.
        followup_questions (list[str]): Exactly three follow-up questions.
        is_related (bool): Whether the question relates to the context.
    Config:
        model_config (ConfigDict): Configuration for the model, including validation
            and JSON schema examples.
    Example:
    {
        "answer": "The study shows...",
        "followup_questions": ["How does this relate to...?", "What are the implications...?", "Can you explain further...?"],
        "is_related": true
    }
    """

    answer: Annotated[
        str,
        Field(
            ...,
            description="Full textual response to the question",
            examples=["The study shows..."],
        ),
    ]

    followup_questions: Annotated[
        list[str],
        Field(
            ...,
            min_length=3,
            max_length=3,
            description="Exactly three follow-up questions",
            examples=[["How...?", "Why...?", "What...?"]],
        ),
    ]

    is_related: Annotated[
        bool,
        Field(
            ...,
            description="Whether the question relates to the context",
        ),
    ]

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
        json_schema_extra={
            "examples": [
                {
                    "answer": "The article demonstrates...",
                    "followup_questions": ["Q1", "Q2", "Q3"],
                    "is_related": True,
                }
            ]
        },
    )


class GenerateAnswerChain(
    Runnable[GenerateAnswerChainInput, GenerateAnswerChainOutput]
):
    """Chain with explicit output type for generating answers from documents and notes."""


@dataclass
class GenerateAnswerReturn:
    answer: str
    followup_questions: list[str]
    is_related: bool


class StreamEvent(BaseModel, Generic[EventType, EventData]):
    event_type: EventType
    data: EventData

    def to_sse(self) -> str:
        return f"event: {self.event_type}\ndata: {self.model_dump_json()}\n\n"


class AnswerStreamEvent(
    StreamEvent[
        Literal["token", "error", "followup_questions", "answer"],
        Union[str, list[Union[str, dict]]],
    ]
):
    pass
