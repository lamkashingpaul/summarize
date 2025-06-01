from typing import Annotated, TypedDict

from attr import dataclass
from langchain_core.runnables import Runnable
from pydantic import BaseModel, ConfigDict, Field

from src.articles.models.article import Article


class NoteOutput(BaseModel):
    content: str
    page_numbers: list[int]


class GenerateNotesChainInput(TypedDict):
    article: Annotated[str, ..., "Article content to generate notes from"]


class GenerateNotesChainOutput(BaseModel):
    """
    GenerateNotesChainOutput schema for the response of a note-generation operation.
    This schema includes a list of generated notes, where each note contains its content and the page numbers where it was found.
    Attributes:
        notes (list[NoteOutput]): List of generated notes with content and page numbers.
    Config:
        model_config (ConfigDict): Configuration for the model, including validation and JSON schema examples.
    Example:
    {
        "notes": [
            {"content": "Note 1 content", "page_numbers": [1, 2]},
            {"content": "Note 2 content", "page_numbers": [3, 4]}
        ]
    }
    """

    notes: Annotated[
        list[NoteOutput],
        Field(
            ...,
            description="List of generated notes with content and page numbers",
            examples=[
                [
                    {"content": "Note 1 content", "page_numbers": [1, 2]},
                    {"content": "Note 2 content", "page_numbers": [3, 4]},
                ]
            ],
        ),
    ]

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
        json_schema_extra={
            "examples": [
                {
                    "notes": [
                        {"content": "Note 1 content", "page_numbers": [1, 2]},
                        {"content": "Note 2 content", "page_numbers": [3, 4]},
                    ]
                }
            ]
        },
    )


class GenerateNotesChain(Runnable[GenerateNotesChainInput, GenerateNotesChainOutput]):
    """Chain with explicit output type for generating notes from an article."""


@dataclass
class GenerateNotesReturn:
    notes: list[NoteOutput]


class CreateNoteDto(BaseModel):
    content: str
    page_numbers: list[int]
    article: Article

    model_config = ConfigDict(arbitrary_types_allowed=True)


CreateNoteDto.model_rebuild()
