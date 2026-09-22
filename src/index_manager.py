from src.embeddings import get_embedding_model

from src.vector_store import (
    load_document_vectorstore,
    create_combined_vectorstore
)


def rebuild_combined_index(
    document_ids
):

    # Remove duplicate document IDs
    document_ids = list(dict.fromkeys(document_ids))

    embeddings = get_embedding_model()

    vectorstores = []

    for document_id in document_ids:

        vectorstore = (
            load_document_vectorstore(
                embeddings,
                document_id
            )
        )

        vectorstores.append(
            vectorstore
        )

    if vectorstores:

        create_combined_vectorstore(
            vectorstores
        )