from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader


def load_pdf(file_path: str):

    pdf_path = Path(
        file_path
    )

    if not pdf_path.exists():

        raise FileNotFoundError(
            f"PDF not found: {file_path}"
        )

    loader = PyPDFLoader(
        str(pdf_path)
    )

    documents = loader.load()

    for document in documents:

        document.metadata[
            "file_name"
        ] = pdf_path.name

    return documents