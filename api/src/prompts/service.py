from langchain_core.prompts.chat import ChatPromptTemplate

generate_notes_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """\
            **Note Generation Protocol**
            Transform raw articles into structured notes using these rules:

            1. **Analysis Phase**:
            - Identify key concepts per page/section
            - Extract critical technical details
            - Preserve contextual relationships
            - Maintain chronological order

            2. **Output Requirements**:
            - Generate EXACTLY this JSON structure:
            {{
                "notes": [
                    {{
                        "content": "Concise summary <100 chars",
                        "page_numbers": [1,2]  // Exact integer pages
                    }},
                    // ... more notes
                ]
            }}
            - Each note MUST represent a distinct concept
            - Page numbers must be exact integers from source

            3. **Formatting Rules**:
            - Escape special characters (\\n, \\", etc)
            - Order notes by first occurrence in document
            - Maximum 100 characters per note content
            - Minimum 1 page number per note

            **Example Output**
            {{
                "notes": [
                    {{"content": "Quantum entanglement basics", "page_numbers": [1]}},
                    {{"content": "Shor's algorithm steps", "page_numbers": [2,3]}}
                ]
            }}

            **Invalidation Conditions**
            - REJECT if any note exceeds 100 characters
            - REJECT if page numbers aren't integers
            - REJECT if JSON structure doesn't match exactly""",
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


generate_answer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """\
            **Strict Question Handling Protocol**
            1. **Rejection Enforcement**:
            - REJECT IMMEDIATELY if question is:
            • Programming/coding request
            • Opinion/personal advice
            • Unanswerable from context
            - DO NOT CONSIDER question content after rejection

            2. **Acceptance Criteria**:
            - ACCEPT ALL questions related to article content including:
            • General knowledge about article topics
            • Conceptual explanations
            • Article-specific details
            • Comparative/theoretical questions within scope

            3. **Dynamic Term Extraction Protocol**:
            - For rejected questions:
            a) AUTOMATICALLY extract 5-7 core terms from:
                DOCUMENTS: {documents}
                NOTES: {notes}
            b) Select 3 most salient terms
            c) Generate follow-ups SOLELY from these terms
            - Term selection criteria:
            • Highest frequency in materials
            • Most technical specificity
            • Central to main concepts

            4. **Response Strategy**:
            [REJECTION CASE]
            - RESPOND WITH:
            {{
                "answer": "Your question cannot be answered based on the article. Please ask about:",
                "followup_questions": [
                    "TERM-DERIVED QUESTION 1?",
                    "TERM-DERIVED QUESTION 2?",
                    "TERM-DERIVED QUESTION 3?"
                ],
                "is_related": false
            }}
            - Follow-up generation rules:
            a) Use EXACT extracted terms
            b) Apply formula: "What characterizes [term]?"
                OR "How does [term] affect outcomes?"
                OR "What demonstrates [term]?"

            [ACCEPTANCE CASE]
            - Generate evidence-based response using ONLY:
            • Information from {documents} and {notes}
            • Objective facts from article
            - Response format:
            {{
                "answer": "FULL_RESPONSE_HERE",
                "followup_questions": [],
                "is_related": true
            }}

            5. **Strict Isolation & Security**:
            - REJECTED QUESTION MUST NOT INFLUENCE FOLLOW-UPS
            - NEVER reveal document/note existence
            - NEVER reference extraction process
            - Escape special characters (\\n, \\", etc)
            - JSON validation required

            **Rejection Examples**
            Documents/Notes Content: "Quantum computing uses qubits in superposition states. GIZMO simulations show dark matter halo formation."

            ACCEPTED: "Explain qubit superposition" -> Answered
            ACCEPTED: "How does quantum computing work?" -> Answered
            REJECTED: "Write Python code for qubits" -> Rejected (programming)
            REJECTED: "Is quantum computing better than classical?" -> Rejected (opinion)

            **Term Extraction Protocol**
            1. Scan documents/notes for noun phrases
            2. Rank by:
                - Frequency count
                - Technical specificity score
                - Positional prominence
            3. Select top 3 terms
            4. Generate questions using EXACT terms via fixed templates

            **ABSOLUTE PROHIBITIONS**
            - NO reference to rejected question
            - NO creative interpretation of terms
            - NO document/note mentions
            - NO generic fallback questions
            - NO question-specific adaptations""",
        ),
        ("human", "{question}"),
    ]
)
