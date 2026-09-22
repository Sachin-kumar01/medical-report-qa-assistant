from pathlib import Path

from langchain_community.vectorstores import FAISS


VECTORSTORE_PATH = Path(
    "vectorstore"
)


COMBINED_INDEX_PATH = (
    VECTORSTORE_PATH / "combined"
)


def create_document_vectorstore(
    documents,
    embeddings,
    document_id
):

    path = (
        VECTORSTORE_PATH
        / document_id
    )

    path.mkdir(
        parents=True,
        exist_ok=True
    )

    vectorstore = FAISS.from_documents(
        documents,
        embeddings
    )

    vectorstore.save_local(
        str(path)
    )

    return vectorstore


def load_document_vectorstore(
    embeddings,
    document_id
):

    path = (
        VECTORSTORE_PATH
        / document_id
    )

    if not path.exists():

        raise FileNotFoundError(
            "Document vectorstore not found."
        )

    return FAISS.load_local(
        str(path),
        embeddings,
        allow_dangerous_deserialization=True
    )


def create_combined_vectorstore(vectorstores):

    if not vectorstores:
        return None

    combined = None

    for vectorstore in vectorstores:

        if combined is None:
            combined = vectorstore
            continue

        # Get documents from current vector store
        documents = list(
            vectorstore.docstore._dict.values()
        )

        # Add documents with fresh IDs
        combined.add_documents(
            documents
        )

    return combined


def load_combined_vectorstore(
    embeddings
):

    if not COMBINED_INDEX_PATH.exists():

        raise FileNotFoundError(
            "Combined vectorstore does not exist."
        )

    return FAISS.load_local(
        str(COMBINED_INDEX_PATH),
        embeddings,
        allow_dangerous_deserialization=True
    )