from src.embeddings import get_embedding_model
from src.vector_store import load_vector_store
from src.llm import get_llm
from src.prompts import SUMMARY_PROMPT


def clean_llm_response(response):

    content = getattr(response, "content", response)

    # Normal string response
    if isinstance(content, str):
        return content.strip()

    # Structured response
    if isinstance(content, list):

        answer_parts = []

        for item in content:

            if isinstance(item, str):
                answer_parts.append(item)

            elif isinstance(item, dict):

                text = item.get("text")

                if text:
                    answer_parts.append(str(text))

        return "\n".join(answer_parts).strip()

    return str(content).strip()


def summarize_report(document_id):

    # Load embedding model
    embeddings = get_embedding_model()

    # Load the selected document's vector store
    vectorstore = load_vector_store(
        embeddings,
        document_id
    )

    # Retrieve relevant report chunks
    documents = vectorstore.similarity_search(
        "medical report patient information laboratory results clinical notes",
        k=10
    )

    context_parts = []

    for document in documents:

        source = document.metadata.get(
            "source",
            "Unknown"
        )

        page = document.metadata.get(
            "page",
            "Unknown"
        )

        content = document.page_content

        context_parts.append(
            f"""
Source: {source}
Page: {page}

Content:
{content}
"""
        )

    context = "\n\n".join(context_parts)

    # Create summary prompt
    prompt = SUMMARY_PROMPT.format(
        context=context
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

    # Extract summary
    summary = response.choices[0].message.content

    if not summary:
        summary = (
            "I could not generate a summary "
            "from the provided report."
        )

    return summary