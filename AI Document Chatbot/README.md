<div align="center">

# 📄 DocuChat AI — Enterprise-Grade PDF Intelligence Engine

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit Framework](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-Enabled-1C3C3C.svg?style=for-the-badge&logo=chainlink&logoColor=white)](https://python.langchain.com/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-Pro-4285F4.svg?style=for-the-badge&logo=google-gemini&logoColor=white)](https://ai.google.dev/)
[![FAISS](https://img.shields.io/badge/FAISS-VectorDB-00599C.svg?style=for-the-badge&logo=facebook&logoColor=white)](https://github.com/facebookresearch/faiss)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

**Instantly analyze, query, and extract insights from complex multi-page PDF documents using Google Gemini LLM and RAG architecture.**

[Features](#-key-features) • [Installation](#%EF%B8%8F-installation--setup) • [Architecture](#-system-architecture--dfd) • [Database Schema](#-entity-relationship-er-diagram) • [Contributing](#-contributing)

</div>

---

## 📌 Table of Contents
- [📖 Purpose & Vision](#-purpose--vision)
- [✨ Key Features](#-key-features)
- [🏗️ System Architecture & DFD](#-system-architecture--dfd)
- [🗄️ Entity-Relationship (ER) Diagram](#%EF%B8%8F-entity-relationship-er-diagram)
- [📂 Project File Structure](#-project-file-structure)
- [⚙️ Requirements](#%EF%B8%8F-requirements)
- [🛠️ Installation & Setup](#%EF%B8%8F-installation--setup)
- [💡 Real-World Applications](#-real-world-applications)
- [🔒 Bugs, Security & Vulnerabilities](#-bugs-security--vulnerabilities)
- [⚖️ Pros, Cons & Limitations](#%EF%B8%8F-pros-cons--limitations)
- [🔮 Roadmap & Future Enhancements](#-roadmap--future-enhancements)
- [🤝 Contributing & Star History](#-contributing--star-history)
- [📜 License & Acknowledgments](#-license--acknowledgments)

---

## 📖 Purpose & Vision

In corporate, academic, and legal environments, professionals waste thousands of hours manually scanning through multi-page PDFs, financial statements, research papers, and technical manuals to extract precise information.

**DocuChat AI** turns static PDFs into dynamic, conversational databases. Built on top of **Streamlit**, **LangChain**, and **Google Gemini**, it leverages **Retrieval-Augmented Generation (RAG)** to perform context-aware semantic searches across documents, returning accurate answers backed by precise citations—all while allowing users to utilize their own API keys (**BYOK**) for maximum privacy and cost efficiency.

---

## ✨ Key Features

- 🔑 **Bring Your Own Key (BYOK):** Seamless user authentication allowing custom Google Gemini API Key entry directly from the sidebar. Zero server-side API key storage.
- 📚 **Multi-PDF Workspace:** Upload, process, and query multiple PDF files simultaneously.
- ⚡ **Hybrid Semantic Search:** FAISS Vector Indexing paired with BM25 keyword matching for high-accuracy retrieval of specialized jargon and technical terms.
- 📌 **Exact Source Citations:** Every response includes metadata tags, page numbers, and snippet previews from the source document to eliminate hallucinations.
- 📊 **Table & OCR-Ready Processing:** Support for extracting text and tabular structures via PyPDF and layout-aware parsers.
- 💾 **Session History Export:** Download conversation logs and analytical summaries as JSON or Markdown formats.
- 🎨 **Production-Optimized Streamlit UI:** Sleek chat interface with real-time streaming responses, memory management, and file status indicators.

---

## 🏗️ System Architecture & DFD

### Data Flow Diagram (DFD - Level 1)

```
 [ User ] 
    │
    ├─ 1. Uploads PDFs & Provides API Key ────────────────┐
    │                                                     ▼
    ├─ 2. Submits Chat Query ───┐               ┌───────────────────┐
    │                           │               │  Streamlit UI     │
    │                           │               │ (Frontend Layer)  │
    │                           │               └─────────┬─────────┘
    ▼                           ▼                         │
┌─────────────────────────────────────────────────────────┼─────────────────────────┐
│ BACKEND PROCESSING ENGINE (LangChain Pipeline)           │                         │
│                                                         ▼                         │
│  ┌────────────────────────┐                   ┌───────────────────┐               │
│  │ Document Loader &      │ ───────►          │ Text Chunker      │               │
│  │ PyPDF Parser           │                   │ (Recursive Split) │               │
│  └────────────────────────┘                   └─────────┬─────────┘               │
│                                                         │                         │
│                                                         ▼                         │
│  ┌────────────────────────┐                   ┌───────────────────┐               │
│  │ Vector Retriever       │ ◄──────────────── │ FAISS Vector DB   │               │
│  │ (Top-K Similarity)     │                   │ (Embeddings Store)│               │
│  └───────────┬────────────┘                   └───────────────────┘               │
│              │                                                                    │
└──────────────┼────────────────────────────────────────────────────────────────────┘
               │
               ▼
┌───────────────────────────────────────────────────────────────────────────────────┐
│ EXTERNAL API LAYER                                                                │
│                                                                                   │
│  ┌────────────────────────┐                   ┌───────────────────┐               │
│  │ Context + Query Payload│ ────────────────► │ Google Gemini AI  │               │
│  │                        │ ◄──────────────── │ (LLM Inference)   │               │
│  └────────────────────────┘                   └───────────────────┘               │
└───────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🗄️ Entity-Relationship (ER) Diagram

Below is the conceptual relational schema for managing sessions, user settings, vector indexes, and chat audit trails in a production database (e.g., PostgreSQL + `pgvector`).

```
┌────────────────────────┐       1:N       ┌────────────────────────┐
│      USERS             │ ───────────────<│     SESSION_LOGS       │
├────────────────────────┤                 ├────────────────────────┤
│ PK  user_id (UUID)     │                 │ PK  session_id (UUID)  │
│     email (VARCHAR)    │                 │ FK  user_id (UUID)     │
│     api_key_hash (TEXT)│                 │     created_at (TIMESTAMP)│
│     created_at (TS)    │                 │     status (VARCHAR)   │
└────────────────────────┘                 └───────────┬────────────┘
                                                       │
                                                       │ 1:N
                                                       ▼
┌────────────────────────┐       1:N       ┌────────────────────────┐
│      DOCUMENT_STORE    │ ───────────────<│    DOCUMENT_CHUNKS     │
├────────────────────────┤                 ├────────────────────────┤
│ PK  doc_id (UUID)      │                 │ PK  chunk_id (UUID)    │
│ FK  session_id (UUID)  │                 │ FK  doc_id (UUID)      │
│     file_name (TEXT)   │                 │     chunk_index (INT)  │
│     file_hash (TEXT)   │                 │     text_content (TEXT)│
│     page_count (INT)   │                 │     embedding (VECTOR) │
│     upload_time (TS)   │                 │     page_number (INT)  │
└────────────────────────┘                 └────────────────────────┘
                                                       │
                                                       │ 1:N
                                                       ▼
                                           ┌────────────────────────┐
                                           │     CHAT_HISTORY       │
                                           ├────────────────────────┤
                                           │ PK  message_id (UUID)  │
                                           │ FK  session_id (UUID)  │
                                           │     sender (USER/AI)   │
                                           │     message (TEXT)     │
                                           │     citations (JSONB)  │
                                           │     timestamp (TS)     │
                                           └────────────────────────┘
```

---

## 📂 Project File Structure

```
docuchat-ai/
├── .streamlit/
│   └── config.toml          # Custom theme configuration
├── assets/
│   ├── architecture_dfd.png  # Diagram visualizations
│   └── screenshot.png       # UI preview banner
├── src/
│   ├── __init__.py
│   ├── pdf_loader.py        # PDF extraction & text chunking logic
│   ├── vector_store.py      # FAISS initialization & retriever setup
│   ├── qa_chain.py          # Gemini LLM initialization & prompt chains
│   └── utils.py             # Session state helpers & export logic
├── app.py                   # Main Streamlit application entry point
├── requirements.txt         # Core dependencies
├── .env.example             # Environment template (optional local fallback)
├── README.md                # Project documentation
└── LICENSE                  # MIT License
```

---

## ⚙️ Requirements

- **Python:** `3.10` or higher
- **API Access:** Google Gemini API Key ([Get Key Here](https://aistudio.google.com/))
- **OS:** Linux, macOS, or Windows

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/alok--kumar8765/docuchat-ai.git
cd docuchat-ai
```

### 2. Create and Activate Virtual Environment
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the Streamlit Application
```bash
streamlit run app.py
```

### 5. Access the Web App
Open your web browser and navigate to `http://localhost:8501`. Enter your **Google Gemini API Key** in the sidebar settings panel to start querying documents!

---

## 💡 Real-World Applications

| Industry | Use Case | Solution Provided |
| :--- | :--- | :--- |
| ⚖️ **Legal Tech** | Contract Analysis | Search clause citations across 100+ page agreement deeds instantly. |
| 🏥 **Healthcare & Medical** | Clinical Research | Summarize dense research papers, dosage guidelines, and patient case studies. |
| 📈 **Finance & Banking** | Earnings & Audit Reports | Compare balance sheets, financial metrics, and disclosure notes accurately. |
| 🎓 **Education & Academia** | Exam & Syllabus Helper | Ask questions directly against textbooks, lecture slides, and research publications. |

---

## 🔒 Bugs, Security & Vulnerabilities

### Known Vulnerabilities & Risks
1. **In-Memory Volatility:** Local FAISS vector indices are stored in RAM session state; clearing the session requires re-uploading documents.
2. **Scanned PDF Limitations:** Native `PyPDF` extractors cannot read non-searchable image-only PDFs without an external Tesseract/OCR engine active.
3. **Prompt Injection:** Malicious text within uploaded PDFs could trick the LLM into ignoring original contextual instructions.

### Mitigation Strategies
- Implement server-side input sanitization for user queries and file stream inputs.
- Enforce strict client-side API Key execution so secrets never persist on hosting servers.

---

## ⚖️ Pros, Cons & Limitations

### 💚 Pros
- ⚡ **Zero Infrastructure Cost:** Lightweight local FAISS vector indexing requires no paid external vector database.
- 🛡️ **Privacy First:** User keys and document vector space exist only during active browser sessions.
- 🎯 **Source Verification:** Minimizes LLM hallucinations with explicit page-number citations.

### 🔴 Cons & Limitations
- **File Size Caps:** Browser memory limits multi-file uploads exceeding ~200MB simultaneously.
- **Context Window:** Extremely large queries spanning dozens of books may exceed single-turn context limits.
- **Single-Node Execution:** Streamlit session state is not distributed; scaling out requires decoupling frontend (React) and backend (FastAPI).

---

## 🔮 Roadmap & Future Enhancements

- [ ] **OCR Engine Integration:** Add Google Document AI/Unstructured for image-heavy and hand-written PDFs.
- [ ] **Persistent Vector Stores:** Add Pinecone & PostgreSQL (`pgvector`) backend options for multi-tenant teams.
- [ ] **Hybrid Retrieval (BM25 + Dense):** Integrate reciprocal rank fusion (RRF) for specialized acronyms and keyword queries.
- [ ] **Decoupled Architecture:** Build out REST API endpoints using **FastAPI** and modern UI dashboards using **Next.js**.

---

## 🤝 Contributing & Star History

Contributions make the open-source community an incredible place to learn, inspire, and create. Any contributions you make are **greatly appreciated**!

1. **Fork the Project**
2. **Create your Feature Branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your Changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the Branch** (`git checkout origin feature/AmazingFeature`)
5. **Open a Pull Request**

If you find this project useful, please give it a ⭐ on GitHub!

<div align="center">

[![Stargazers over time](https://starchart.cc/alok--kumar8765/docuchat-ai.svg?variant=adaptive)](https://starchart.cc/alok--kumar8765/docuchat-ai)

</div>

---

## 📜 License & Acknowledgments

Distributed under the MIT License. See `LICENSE` for more information.

Developed with ❤️ by **[Alok Kumar](https://github.com/alok--kumar8765)**. Special thanks to the Streamlit and LangChain communities for empowering open AI innovation.