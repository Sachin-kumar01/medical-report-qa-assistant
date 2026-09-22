# 🩺 Medical Report Q&A Assistant

A **RAG-based Medical Report Q&A Assistant** that allows users to upload one or more medical PDF reports and ask questions about the information contained in those reports.

The application uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant sections from uploaded reports before generating an answer with an LLM.

The application also provides **source document and page references** for retrieved information.

> ⚠️ **Medical Safety Disclaimer:** This project is for educational and demonstration purposes only. It does not provide medical diagnosis, treatment, or professional medical advice. Always consult a qualified healthcare professional for medical decisions.

---

## 🚀 Features

- 📄 Upload one or multiple medical PDF reports
- 🔍 Extract text from PDF reports
- ✂️ Split documents into smaller chunks
- 🧠 Generate semantic embeddings
- 🗂️ Store embeddings using FAISS
- 🔎 Perform semantic similarity search
- 🤖 Generate answers using an LLM through OpenRouter
- 💬 Follow-up questions and conversational history
- 📚 Multi-document question answering
- 🔀 Compare information across multiple reports
- 📌 Display source document and page numbers
- 📊 Dashboard with document statistics
- 📝 Generate medical report summaries
- 🗑️ Delete uploaded documents
- 🛡️ Context-grounded answers to reduce unsupported information

---

# 🏗️ Architecture

```text
                    ┌──────────────────────┐
                    │     User Uploads     │
                    │      Medical PDF     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      PDF Loader      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Text Chunking     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     Embeddings       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    FAISS Vector DB   │
                    └──────────┬───────────┘
                               │
                         User Question
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Similarity Search   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Relevant PDF Chunks  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    LLM + Prompt      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Grounded Answer +    │
                    │ Source/Page Details  │
                    └──────────────────────┘
```

---

# 🛠️ Tech Stack

## Programming Language

- Python

## Frontend / UI

- Streamlit

## RAG

- LangChain
- FAISS
- Sentence Transformers
- Semantic Search

## LLM

- OpenRouter
- OpenAI-compatible API

## PDF Processing

- PDF document loader
- Text extraction
- Document chunking

## Environment Management

- python-dotenv

---

# 📂 Project Structure

```text
Medical Report Q&A Assistant/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
├── .env
│
├── data/
│   └── uploads/
│
├── vectorstore/
│   ├── combined/
│   └── document-specific vector stores
│
└── src/
    ├── __init__.py
    ├── embeddings.py
    ├── vector_store.py
    ├── pdf_loader.py
    ├── text_splitter.py
    ├── rag_pipeline.py
    ├── llm.py
    ├── prompts.py
    ├── summarizer.py
    ├── document_manager.py
    ├── index_manager.py
    └── medical_extractor.py
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Then:

```bash
cd "Medical Report Q&A Assistant"
```

---

# 2. Create Virtual Environment

For Windows:

```bash
py -3.13 -m venv venv
```

Activate the environment:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell gives an execution-policy error, run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again:

```powershell
.\venv\Scripts\Activate.ps1
```

---

# 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the root project folder.

```env
OPENROUTER_API_KEY=YOUR_OPENROUTER_API_KEY
```

Example:

```env
OPENROUTER_API_KEY=sk-or-v1-YOUR_KEY_HERE
```

Do not put your actual API key inside the source code.

---

# 🔐 API Key Security

Make sure `.env` is included in `.gitignore`.

Example `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc

data/uploads/
vectorstore/
.streamlit/
```

### Important

Never upload API keys, passwords, tokens, or other secrets to GitHub.

If an API key is accidentally exposed publicly:

1. Revoke the old key.
2. Generate a new key.
3. Update your `.env` file.
4. Make sure `.env` is added to `.gitignore`.

---

# ▶️ Run the Application

After activating the virtual environment:

```bash
streamlit run app.py
```

The application will open in your browser.

---

# 🧠 How the RAG System Works

The application follows a **Retrieval-Augmented Generation (RAG)** architecture.

## Step 1 — Upload PDF

The user uploads one or more medical reports through the Streamlit interface.

```text
Medical Report PDF
        ↓
Streamlit Upload
```

---

## Step 2 — PDF Processing

The application extracts text from the uploaded PDF.

```text
PDF
 ↓
Text Extraction
```

---

## Step 3 — Text Chunking

The extracted content is divided into smaller chunks.

```text
Large Document
      ↓
Small Text Chunks
```

Chunking allows the application to retrieve only the relevant sections instead of sending the complete report to the LLM.

---

## Step 4 — Embeddings

Each text chunk is converted into a numerical vector using an embedding model.

```text
Text Chunk
    ↓
Embedding Model
    ↓
Vector
```

---

## Step 5 — FAISS Vector Store

The generated vectors are stored in FAISS.

```text
Embeddings
    ↓
FAISS
    ↓
Vector Search
```

---

## Step 6 — User Question

The user asks a question.

Example:

```text
What is the patient's hemoglobin level?
```

---

## Step 7 — Similarity Search

The application converts the question into a vector and searches FAISS for the most relevant document chunks.

```text
User Question
      ↓
Question Embedding
      ↓
FAISS Similarity Search
      ↓
Relevant Chunks
```

---

## Step 8 — LLM Generation

The retrieved chunks are provided to the LLM together with the user's question.

```text
Retrieved Context
       +
User Question
       ↓
      LLM
       ↓
Generated Answer
```

---

## Step 9 — Source Information

The application displays the document and page from which the retrieved information came.

Example:

```text
📄 medical_report_2.pdf — Page 1
```

---

# 💬 Example Questions

After uploading a medical report, users can ask:

```text
What is the patient's hemoglobin level?
```

```text
What is the fasting glucose value?
```

```text
What is the patient's cholesterol level?
```

```text
Which values are outside the reference range?
```

```text
Summarize this medical report.
```

```text
What information is available about the lipid profile?
```

---

# 📚 Multi-Document Question Answering

The application supports multiple medical reports.

Example:

```text
Report 1
Report 2
Report 3
```

Users can select the reports they want to search.

Then they can ask questions such as:

```text
Compare the hemoglobin levels across the selected reports.
```

or:

```text
Which report has the highest LDL value?
```

The RAG pipeline retrieves relevant information from the selected documents.

---

# 📌 Source References

The application keeps metadata for retrieved document chunks.

The UI displays:

```text
📄 medical_report_2.pdf — Page 1
📄 medical_report_3.pdf — Page 1
```

This helps users understand where the information used for an answer came from.

---

# 📝 Report Summarization

The project also includes a report summarization pipeline.

The summarizer:

1. Loads the document vector store.
2. Retrieves relevant report information.
3. Creates a context from the retrieved chunks.
4. Sends the context to the LLM.
5. Generates a concise report summary.

Example:

```text
User uploads report
        ↓
Document Processing
        ↓
Vector Search
        ↓
Relevant Medical Information
        ↓
LLM
        ↓
Report Summary
```

---

# 🗑️ Document Management

The application provides document management functionality.

Users can:

- View uploaded reports
- Select reports for querying
- Delete reports
- Re-upload reports
- Process multiple reports
- View document statistics

The dashboard displays:

```text
Documents
Total Pages
Indexed Chunks
```

---

# 🧪 Testing

The application has been tested with:

- Single PDF upload
- Multiple PDF upload
- Duplicate document processing
- Document selection
- Factual questions
- Concept questions
- Missing information
- Follow-up questions
- Report summarization
- Multi-document comparison
- Source/page references
- PDF deletion
- PDF re-upload
- Edge cases
- UI interactions

---

# 🛡️ Medical Safety

This application is an **educational AI/RAG project**.

It should not be used as a replacement for:

- Doctors
- Medical professionals
- Clinical diagnosis
- Medical treatment decisions
- Emergency medical services

The system is designed to answer questions based on information retrieved from uploaded reports.

Users should consult qualified healthcare professionals for actual medical decisions.

---

# 🔮 Future Improvements

Possible future improvements include:

- 🔐 User authentication
- 👤 User-specific document libraries
- 💾 Database-based document management
- 📊 Medical report visualization
- 📈 Lab-value trend charts
- 🔎 Advanced medical value extraction
- 🧠 Retrieval reranking
- ⚡ Streaming LLM responses
- 🌐 Cloud deployment
- 📱 Responsive UI
- 🩺 Additional medical safety guardrails
- 🗃️ Support for additional document formats
- 🔐 Better privacy and access controls

---

# 📊 Current Project Workflow

```text
User
 │
 │ Upload Medical PDF
 ▼
Streamlit Application
 │
 ▼
PDF Loader
 │
 ▼
Text Splitter
 │
 ▼
Embedding Model
 │
 ▼
FAISS Vector Store
 │
 │
 │ User asks question
 ▼
Similarity Search
 │
 ▼
Relevant Document Chunks
 │
 ▼
Prompt + Context
 │
 ▼
OpenRouter LLM
 │
 ▼
Answer
 │
 ▼
Source Document + Page
```

---

# 🎯 Resume Project Description

### Medical Report Q&A Assistant | Python, Streamlit, LangChain, FAISS, LLMs

- Built a RAG-based medical document Q&A assistant that allows users to upload and query multiple PDF reports using semantic retrieval and LLMs.
- Implemented PDF ingestion, text chunking, embeddings, FAISS vector search, and context-grounded response generation.
- Added multi-document querying, conversational follow-up questions, report summarization, and source/page references for retrieved information.

---

# 🤖 Current LLM Configuration

The current tested OpenRouter configuration uses:

```text
nex-agi/nex-n2.5-mini:free
```

Free-model availability and rate limits can change over time, so the configured model may need to be updated in the future.

---

# 📦 Requirements

The main dependencies used by the project include:

```text
torch
transformers
streamlit
sentence-transformers
faiss-cpu
langchain
langchain-google-genai
openai
python-dotenv
```

For the exact versions used in the project, check:

```text
requirements.txt
```

---

# 👨‍💻 Author

**Sachin Kumar**

B.Tech — Computer Science & Engineering

GitHub:

```text
YOUR_GITHUB_PROFILE
```

LinkedIn:

```text
YOUR_LINKEDIN_PROFILE
```

---

# ⭐ Project Goal

The goal of this project is to demonstrate how **Retrieval-Augmented Generation (RAG)** can be used to build a document-grounded AI assistant capable of answering questions from user-uploaded medical reports while providing source references for retrieved information.

---

## ⚠️ Disclaimer

This project is intended for **educational and demonstration purposes only**.

It is not a medical diagnostic system and should not be used to make medical decisions.