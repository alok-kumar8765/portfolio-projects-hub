<div align="center">

# 👔 Recruitment Analytics Platform & AI Resume Screener

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red.svg)](https://streamlit.io/)
[![SQLite](https://img.shields.io/badge/Database-SQLite3-lightgrey.svg)](https://www.sqlite.org/)
[![GitHub Creator](https://img.shields.io/badge/GitHub-alok--kumar8765-orange.svg)](https://github.com/alok--kumar8765)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

*An enterprise-grade, full-stack recruitment dashboard featuring role-based portals, automated AI resume keyword matching, salary/budget tracking, and a Kanban hiring pipeline.*

</div>

---

## 📖 Table of Contents
1. [Purpose & Use](#-purpose--use)
2. [Features](#-features)
3. [System Architecture & Diagrams](#-system-architecture--diagrams)
   - [Data Flow Diagram (DFD)](#data-flow-diagram-dfd)
   - [Entity-Relationship (ER) Diagram](#entity-relationship-er-diagram)
4. [File Structure](#-file-structure)
5. [Requirements](#-requirements)
6. [Installation & Setup](#-installation--setup)
7. [Pros & Cons](#-pros--cons)
8. [Limitations](#-limitations)
9. [Bugs & Vulnerabilities](#-bugs--vulnerabilities)
10. [Future Updates](#-future-updates)
11. [Contributing](#-contributing)
12. [Author & Acknowledgments](#-author--acknowledgments)

---

## 🎯 Purpose & Use

### **Purpose**
Modern recruitment is overwhelmed by manual candidate screening, scattered communication, and lack of real-time hiring metrics. The **Recruitment Analytics Platform** bridges the gap between candidates and HR teams by providing a unified, lightning-fast system to post jobs, parse CVs, calculate automated match scores, and track candidate progress visually.

### **Use Cases**
- **HR Managers & Recruiters:** Post job descriptions with precise salary budgets and required tech stacks, review applicants, and accept/reject candidates instantly.
- **Job Seekers:** Access a dedicated candidate portal to submit CVs/resumes and get instant AI skill-matching feedback.
- **Hiring Teams:** Track recruitment pipelines using an interactive Kanban board and analyze hiring metrics via Plotly dashboards.

---

## 🚀 Features

- **Dual-Portal Architecture:** Seamlessly toggle between the *HR & Admin Dashboard* and the *Candidate Application Portal*.
- **AI Resume Screening & Keyword Match Engine:** Upload PDF/TXT CVs; the system extracts skills, compares them against job requirements, and calculates an instant Match Score ($\\%$).
- **HR Job Posting with Compensation & Tech Stacks:** Define job titles, departments, vacancy counts, salary ranges, and comma-separated required tools.
- **Interactive Approval Workflows:** Operational `Accept` and `Cancel` buttons directly linked to persistent database records.
- **Visual Kanban Hiring Pipeline:** Drag-and-drop or click to move candidates across stages (*Applied $\rightarrow$ Screening $\rightarrow$ Interview $\rightarrow$ Offered*).
- **Persistent SQLite Storage:** All data is safely stored in a local SQLite3 database (`recruitment.db`), preventing data loss on browser refresh.

---

## 🏗️ System Architecture & Diagrams

### **Data Flow Diagram (DFD)**
```text
 [ Candidate ] ──(Uploads CV / Skills)──> [ Candidate Portal ]
                                                 │
                                           (AI Match Engine)
                                                 │
                                                 ▼
 [ HR Manager ] ──(Posts Job & Budget)──> [ SQLite Database ] <──(Updates Status)── [ HR Dashboard ]
```

### **Entity-Relationship (ER) Diagram**
```text
+------------------------+          +-------------------------+
|         JOBS           |          |       CANDIDATES        |
+------------------------+          +-------------------------+
| PK  id                 | 1      N | PK  id                  |
|     title              |<---------| FK  job_id              |
|     department         |          |     name                |
|     experience         |          |     email               |
|     vacancies          |          |     skills              |
|     salary             |          |     match_score         |
|     tools              |          |     stage               |
|     description        |          |     status              |
|     date / status      |          +-------------------------+
+------------------------+
```

---

## 📂 File Structure

```text
CV-Short-List-App/
│
├── app.py               # Main monolithic Streamlit application
├── recruitment.db       # Local SQLite3 database (auto-generated)
├── requirements.txt     # Python package dependencies
└── README.md            # Project documentation
```

---

## 📦 Requirements

- Python `3.8` or higher
- Streamlit `1.28+`
- Pandas `2.0+`
- Plotly `5.0+`

---

## ⚙️ Installation & Setup

Follow these steps to set up the project locally on your machine:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/alok--kumar8765/CV-Short-List-App.git
   cd CV-Short-List-App
   ```

2. **Create a Virtual Environment (Recommended):**
   ```bash
   python -m venv env
   # On Windows:
   env\Scripts\activate
   # On macOS/Linux:
   source env/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install streamlit pandas plotly
   ```

4. **Run the Application:**
   ```bash
   streamlit run app.py
   ```

5. **Access the App:**
   Open your browser and navigate to `http://localhost:8501`.

---

## ⚖️ Pros & Cons

### **Pros**
- **Zero Configuration DB:** Uses SQLite3 out-of-the-box with zero external database server setup required.
- **Blazing Fast UI:** Built with Streamlit for rapid Python-native prototyping and deployment.
- **Complete Workflow:** Covers the entire lifecycle from job creation to candidate application and hiring pipeline tracking.

### **Cons**
- **Monolithic Architecture:** All frontend and backend logic resides in a single file (`app.py`), which can become harder to scale for massive enterprise apps.
- **Local Database:** SQLite is file-based and not optimized for concurrent multi-server cloud scaling without external volume mounts.

---

## ⚠️ Limitations
- The resume parser uses keyword token matching rather than advanced Large Language Model (LLM) vector embeddings.
- Email notifications and calendar syncs are currently simulated via UI toasts rather than live SMTP/Google Calendar API integrations.

---

## 🐛 Bugs & Vulnerabilities
- **File Upload Encoding:** Uploading binary formats other than plain text or standard PDFs may occasionally trigger text decoding warnings if unstructured.
- **Concurrency:** SQLite handles limited concurrent writes; high-volume simultaneous candidate applications might require migration to PostgreSQL.

---

## 🔮 Future Updates
- [ ] Migrate SQLite backend to PostgreSQL with SQLAlchemy ORM.
- [ ] Integrate OpenAI / Hugging Face API for deep semantic resume embeddings (ChromaDB).
- [ ] Add automated SMTP email notifications upon candidate acceptance/rejection.
- [ ] Implement OAuth2 Role-Based Access Control (RBAC) for secure HR logins.

---

## 🤝 Contributing
Contributions are always welcome! If you'd like to improve this project:
1. Fork the repository (`https://github.com/alok--kumar8765/CV-Short-List-App`)
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## ⭐ Thanks & Acknowledgments
A special thanks to everyone supporting open-source Python development! 

If you find this project useful or interesting, please consider giving it a ⭐ on GitHub!

**Created with ❤️ by [Alok Kumar](https://github.com/alok--kumar8765)**