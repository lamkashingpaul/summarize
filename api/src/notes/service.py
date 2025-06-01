from typing import cast

from langchain_core.documents import Document
from langchain_deepseek import ChatDeepSeek

from src.articles.models.article import Article
from src.database.service import SessionDep
from src.embeddings.utils import format_documents_to_string
from src.notes.models.note import Note
from src.notes.schemas.internals import (
    CreateNoteDto,
    GenerateNotesChain,
    GenerateNotesChainOutput,
)
from src.prompts.service import generate_notes_prompt


async def save_notes(
    documents: list[Document], article: Article, session: SessionDep
) -> list[Note]:
    documents_as_string = format_documents_to_string(documents)
    model = ChatDeepSeek(model="deepseek-chat", temperature=0.0)

    chain = cast(
        GenerateNotesChain,
        generate_notes_prompt | model.with_structured_output(GenerateNotesChainOutput),
    )

    response = await chain.ainvoke({"article": documents_as_string})

    notes = [
        Note(
            **CreateNoteDto(
                content=note.content,
                page_numbers=note.page_numbers,
                article=article,
            ).model_dump()
        )
        for note in response.notes
    ]

    session.add_all(notes)
    return notes
