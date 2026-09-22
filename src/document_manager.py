import json
from pathlib import Path


DOCUMENTS_FILE = Path(
    "data/documents.json"
)


def initialize_document_file():

    DOCUMENTS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if not DOCUMENTS_FILE.exists():

        with open(
            DOCUMENTS_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                [],
                file,
                indent=4
            )


def get_documents():

    initialize_document_file()

    with open(
        DOCUMENTS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def save_documents(documents):

    initialize_document_file()

    with open(
        DOCUMENTS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            documents,
            file,
            indent=4
        )


def add_document(
    document_id,
    file_name,
    pages,
    chunks
):

    documents = get_documents()

    document = {
        "id": document_id,
        "file_name": file_name,
        "pages": pages,
        "chunks": chunks
    }

    documents.append(
        document
    )

    save_documents(
        documents
    )


def delete_document(document_id):

    documents = get_documents()

    documents = [
        document
        for document in documents
        if document["id"] != document_id
    ]

    save_documents(
        documents
    )


def clear_documents():

    save_documents([])