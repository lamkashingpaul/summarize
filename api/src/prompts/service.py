from langchain_core.messages import AIMessageChunk
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.tools import tool

from src.articles.models import Note

notes_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "ai",
            """
            You are a summarization assistant.

            Your task is to read the article and extract key notes directly.

            If the article is long, create multiple notes, each focused on a specific section or main idea for that page. Summarize the content in your own words with text referenced from the article.

            Make sure enough notes are summarized such that all notes together comprehensively cover the entire article.

            For each note, include the summarized text and the corresponding page numbers. Format the notes and page numbers into a structured format.

            Begin summarizing the article now.
            """,
        ),
        ("human", "Article: {article}"),
    ]
)


@tool
def format_note(note: str, page_numbers: list[int]) -> str:
    """
    Format the note and page numbers into a structured format.
    Args:
        note (str): The note text.
        page_numbers (list[int]): The list of page numbers associated with the note.
    Returns:
        str: The formatted note and page numbers.
    """
    return f"Note: {note}\nPage Numbers: {', '.join(map(str, page_numbers))}"


def format_output(output: AIMessageChunk) -> list[Note]:
    toolCalls = output.tool_calls
    notes: list[Note] = []

    for toolCall in toolCalls:
        if toolCall["name"] == format_note.name:
            note = toolCall["args"]["note"]
            page_numbers = toolCall["args"]["page_numbers"]
            notes.append(Note(note=note, page_numbers=page_numbers))

    return notes
