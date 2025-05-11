from langchain_core.messages import AIMessageChunk
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.tools import tool

from src.articles.models.note import Note

notes_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """\
            **Note Generation Protocol**
            Transform raw articles into structured notes using these rules:

            1. Analysis Phase:
            - Identify key concepts per page/section
            - Extract critical technical details
            - Preserve contextual relationships

            2. Formatting Phase:
            - Use `format_note` tool for EACH distinct concept
            - Page numbers must be exact integers
            - Maintain chronological order

            **Output Requirements**
            {{
                "note": "Concise summary <100 chars",
                "page_numbers": [1,2]  # Exact source pages
            }}
            """,
        ),
        (
            "human",
            """\
            Process this article:
            {article}
            """,
        ),
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


def format_output_notes(output: AIMessageChunk) -> list[Note]:
    toolCalls = output.tool_calls
    notes: list[Note] = []

    for toolCall in toolCalls:
        if toolCall["name"] == format_note.name:
            note = toolCall["args"]["note"]
            page_numbers = toolCall["args"]["page_numbers"]
            notes.append(Note(note=note, page_numbers=page_numbers))

    return notes


answer_question_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """\
            **Question Handling Protocol**
            Execute these steps in order:

            1. Relevance Check:
            - Analyze if the question asked by user relates to either:
                a) <<DOCUMENTS>> {documents}
                b) <<NOTES>> {notes}
            - No partial matches → Mark as unrelated

            2. Response Strategy:
            [If Related]
            - Cross-reference sources
            - Answer using BOTH documents/notes
            - Create gap-focused follow-ups

            [If Unrelated]
            - Do NOT mention documents/notes existence
            - State question mismatch
            - Suggest article-specific follow-ups

            3. Mandatory Formatting:
            - ALWAYS use 'format_answer_to_question' tool
            - Follow exact output structure

            **Source Analysis Rules**
            - Consider related if:
                • Any term/phrase match
                • Conceptual similarity
                • Implied context
            - Unrelated threshold: Zero matches

            **Example Outputs**
            Related Question:
            {{
                "answer": "The study methodology combines... [Conflict: Notes emphasize limitations]",
                "followup_questions": ["How were limitations addressed?", "Why methodology choices?"]
            }}

            Unrelated Question:
            {{
                "answer": "This question appears unrelated to the article's focus on <ARTICLE_TOPIC>",
                "followup_questions": ["What were the key findings about <TOPIC>?", "How does <ARTICLE_CONCEPT> work?"]
            }}
            """,
        ),
        ("human", "{question}"),
    ]
)


@tool
def format_answer_to_question(
    answer: str, followup_questions: list[str]
) -> tuple[str, list[str]]:
    """
    Format the answer and follow-up questions into a structured format.
    Args:
        answer (str): The answer text.
        followup_questions (list[str]): The list of follow-up questions.
    Returns:
        tuple[str, list[str]]: The formatted answer and follow-up questions.
    """
    return answer, followup_questions


def format_output_answer_to_question(output: AIMessageChunk) -> tuple[str, list[str]]:
    toolCalls = output.tool_calls
    answer = ""
    followup_questions: list[str] = []

    for toolCall in toolCalls:
        if toolCall["name"] == format_answer_to_question.name:
            answer = toolCall["args"]["answer"]
            followup_questions = toolCall["args"]["followup_questions"]
            break

    return answer, followup_questions
