from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.messages import AIMessageChunk
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from src.articles.models import Note

notes_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "ai",
            """
            Please read and summarize the following article. Generate notes that cover the entire article, ensuring that a complete understanding is guaranteed after reading all the notes. Each note should be structured as follows:

            - A summary of a key point or concept discussed in the article.
            - Include the page numbers where the information can be found.

            The notes should be in this format:

            [
                {{
                    "note": "The author discusses the importance of XYZ in the context of ABC.",
                    "page_numbers": [1, 2]
                }},
                {{
                    "note": "The author describes the method used to measure XYZ.",
                    "page_numbers": [3]
                }}
            ]
            """,
        ),
        ("human", "Article: {article}"),
    ]
)


class format_notes(BaseModel):
    note: str = Field(..., description="The note extracted from the article.")
    page_numbers: list[int] = Field(
        ..., description="List of page numbers where the note is found."
    )


def format_output(output: AIMessageChunk) -> list[Note]:
    toolCalls = output.tool_calls
    notes: list[Note] = []

    for toolCall in toolCalls:
        if toolCall["name"] == format_notes.__name__:
            note = toolCall["args"]["note"]
            page_numbers = toolCall["args"]["page_numbers"]
            notes.append(Note(note=note, page_numbers=page_numbers))

    return notes
