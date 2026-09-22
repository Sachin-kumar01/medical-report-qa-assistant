from src.embeddings import get_embedding_model
from src.vector_store import load_document_vectorstore
from src.llm import get_llm
from src.prompts import SYSTEM_PROMPT


def answer_question(
    question,
    document_ids,
    chat_history=""
):

    if not document_ids:
        raise ValueError(
            "No documents selected."
        )

    embeddings = get_embedding_model()

    all_documents = []

    for document_id in document_ids:

        vectorstore = load_document_vectorstore(
            embeddings,
            document_id
        )

        documents = vectorstore.similarity_search(
            question,
            k=4
        )

        all_documents.extend(
            documents
        )

    # Keep the most relevant documents
    documents = all_documents[:8]

    context_parts = []

    for document in documents:

        file_name = document.metadata.get(
            "file_name",
            "Unknown document"
        )

        page = document.metadata.get(
            "page",
            "Unknown"
        )

        content = document.page_content

        context_parts.append(
            f"""
DOCUMENT: {file_name}

PAGE: {page}

CONTENT:

{content}
"""
        )

    context = "\n\n".join(
        context_parts
    )

    prompt = SYSTEM_PROMPT.format(
        context=context,
        chat_history=chat_history,
        question=question
    )

    # Get OpenRouter client
    llm = get_llm()

    # Call OpenRouter
    response = llm.chat.completions.create(
        model="nex-agi/nex-n2.5-mini:free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # Debug: OpenRouter response
    print(
        "\n========== OPENROUTER RESPONSE =========="
    )
    print(response)
    print(
        "=========================================\n"
    )

    # Extract answer
    answer = response.choices[0].message.content

    # Debug: final answer
    print(
        "\n========== ANSWER =========="
    )
    print(answer)
    print(
        "============================\n"
    )

    if not answer:
        answer = (
            "I could not generate an answer "
            "from the provided report."
        )

    return answer, documents