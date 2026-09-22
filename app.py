import streamlit as st
from pathlib import Path
import hashlib
import shutil

from src.pdf_loader import load_pdf
from src.text_splitter import split_documents
from src.embeddings import get_embedding_model

from src.vector_store import (
    create_document_vectorstore
)

from src.rag_pipeline import answer_question

from src.document_manager import (
    get_documents,
    add_document,
    delete_document
)

from src.index_manager import (
    rebuild_combined_index
)

from src.medical_extractor import (
    extract_medical_values
)


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Medical Report AI",
    page_icon="🩺",
    layout="wide"
)


# ==================================================
# SESSION STATE
# ==================================================

if "chat_history" not in st.session_state:

    st.session_state.chat_history = []


if "selected_documents" not in st.session_state:

    st.session_state.selected_documents = []


# ==================================================
# DIRECTORIES
# ==================================================

UPLOAD_DIR = Path(
    "data/uploads"
)

VECTORSTORE_DIR = Path(
    "vectorstore"
)

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ==================================================
# HEADER
# ==================================================

st.title(
    "🩺 Medical Report AI Assistant"
)

st.caption(
    "Multi-document RAG-powered medical report analysis"
)


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.header(
        "📁 Document Manager"
    )

    uploaded_files = st.file_uploader(
        "Upload Medical Reports",
        type=["pdf"],
        accept_multiple_files=True
    )


    if uploaded_files:

        if st.button(
            "🚀 Process Documents",
            type="primary",
            use_container_width=True
        ):

            with st.spinner(
                "Processing documents..."
            ):

                embeddings = (
                    get_embedding_model()
                )

                processed_ids = []

                for uploaded_file in uploaded_files:

                    file_bytes = (
                        uploaded_file.getbuffer()
                    )

                    document_id = hashlib.md5(
                        file_bytes
                    ).hexdigest()

                    save_path = (
                        UPLOAD_DIR
                        / uploaded_file.name
                    )

                    with open(
                        save_path,
                        "wb"
                    ) as file:

                        file.write(
                            file_bytes
                        )

                    documents = load_pdf(
                        str(save_path)
                    )

                    chunks = split_documents(
                        documents
                    )

                    create_document_vectorstore(
                        chunks,
                        embeddings,
                        document_id
                    )

                    add_document(
                        document_id,
                        uploaded_file.name,
                        len(documents),
                        len(chunks)
                    )

                    processed_ids.append(
                        document_id
                    )

                all_documents = (
                    get_documents()
                )

                all_ids = [
                    document["id"]
                    for document in all_documents
                ]

                rebuild_combined_index(
                    all_ids
                )

            st.success(
                f"Processed {len(uploaded_files)} document(s)."
            )

            st.session_state.chat_history = []


    st.divider()


    # ==================================================
    # DOCUMENT LIST
    # ==================================================

    documents = get_documents()

    st.subheader(
        "📚 Your Documents"
    )


    selected_ids = []


    for index, document in enumerate(documents):

        checked = st.checkbox(
            document["file_name"],
            value=True,
            key=f"doc_{index}_{document['id']}"
        )

        if checked:

            selected_ids.append(
                document["id"]
            )


    st.session_state.selected_documents = (
        selected_ids
    )


# ==================================================
# MAIN CONTENT
# ==================================================

documents = get_documents()


if not documents:

    st.info(
        "Upload one or more medical reports "
        "from the sidebar to begin."
    )

else:

    # ==================================================
    # DASHBOARD
    # ==================================================

    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Documents",
            len(documents)
        )


    with col2:

        total_pages = sum(
            document["pages"]
            for document in documents
        )

        st.metric(
            "Total Pages",
            total_pages
        )


    with col3:

        total_chunks = sum(
            document["chunks"]
            for document in documents
        )

        st.metric(
            "Indexed Chunks",
            total_chunks
        )


    st.divider()


    # ==================================================
    # TABS
    # ==================================================

    tab_chat, tab_docs = st.tabs(
        [
            "💬 AI Assistant",
            "📚 Documents"
        ]
    )


    # ==================================================
    # CHAT
    # ==================================================

    with tab_chat:

        if not selected_ids:

            st.warning(
                "Select at least one document "
                "from the sidebar."
            )

        else:

            st.subheader(
                "💬 Ask About Your Reports"
            )

            st.caption(
                f"Searching across "
                f"{len(selected_ids)} selected document(s)"
            )


            # Display history

            for message in (
                st.session_state.chat_history
            ):

                with st.chat_message(
                    message["role"]
                ):

                    st.markdown(
                        message["content"]
                    )


            question = st.chat_input(
                "Ask a question about your reports..."
            )


            if question:

                st.session_state.chat_history.append(
                    {
                        "role": "user",
                        "content": question
                    }
                )


                with st.chat_message(
                    "user"
                ):

                    st.markdown(
                        question
                    )


                history = ""

                for message in (
                    st.session_state.chat_history[:-1]
                ):

                    history += (
                        f'{message["role"]}: '
                        f'{message["content"]}\n'
                    )


                with st.chat_message(
                    "assistant"
                ):

                    with st.spinner(
                        "Searching reports..."
                    ):

                        try:

                            answer, sources = (
                                answer_question(
                                    question,
                                    selected_ids,
                                    history
                                )
                            )

                            st.markdown(
                                answer
                            )


                            # =================================
                            # SOURCES
                            # =================================

                            st.markdown(
                                "### 📚 Sources"
                            )

                            shown_sources = set()


                            for document in sources:

                                file_name = (
                                    document.metadata.get(
                                        "file_name",
                                        "Unknown"
                                    )
                                )

                                page = (
                                    document.metadata.get(
                                        "page",
                                        "Unknown"
                                    )
                                )


                                try:

                                    page_number = (
                                        int(page) + 1
                                    )

                                except:

                                    page_number = page


                                source_key = (
                                    file_name,
                                    page_number
                                )


                                if (
                                    source_key
                                    not in shown_sources
                                ):

                                    st.caption(
                                        f"📄 "
                                        f"{file_name} "
                                        f"— Page "
                                        f"{page_number}"
                                    )

                                    shown_sources.add(
                                        source_key
                                    )


                            st.session_state.chat_history.append(
                                {
                                    "role": "assistant",
                                    "content": answer
                                }
                            )


                        except Exception as error:

                            st.error(
                                f"Error: {error}"
                            )


    # ==================================================
    # DOCUMENTS
    # ==================================================

    with tab_docs:

        st.subheader(
            "📚 Document Library"
        )


        for index, document in enumerate(documents):

            col1, col2, col3, col4 = st.columns(
                [
                    4,
                    2,
                    2,
                    1
                ]
            )


            with col1:

                st.write(
                    f"📄 **{document['file_name']}**"
                )


            with col2:

                st.write(
                    f"{document['pages']} pages"
                )


            with col3:

                st.write(
                    f"{document['chunks']} chunks"
                )


            with col4:

                if st.button(
                    "🗑️",
                    key=f"delete_{index}_{document['id']}"
                ):

                    # Delete uploaded PDF

                    pdf_path = (
                        UPLOAD_DIR
                        / document["file_name"]
                    )

                    if pdf_path.exists():

                        pdf_path.unlink()


                    # Delete vectorstore

                    vector_path = (
                        VECTORSTORE_DIR
                        / document["id"]
                    )

                    if vector_path.exists():

                        shutil.rmtree(
                            vector_path
                        )


                    # Delete metadata

                    delete_document(
                        document["id"]
                    )


                    # Rebuild combined index

                    remaining = (
                        get_documents()
                    )

                    remaining_ids = [
                        item["id"]
                        for item in remaining
                    ]


                    if remaining_ids:

                        rebuild_combined_index(
                            remaining_ids
                        )

                    else:

                        combined_path = (
                            VECTORSTORE_DIR
                            / "combined"
                        )

                        if combined_path.exists():

                            shutil.rmtree(
                                combined_path
                            )


                    st.rerun()