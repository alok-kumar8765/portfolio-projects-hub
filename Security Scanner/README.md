# 🛡️ AI Code Security Scanner

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Profile](https://img.shields.io/badge/GitHub-alok--kumar8765-181717?logo=github)](https://github.com/alok--kumar8765)

---

## 📌 Description

The **AI Code Security Scanner** is a developer-focused static application security testing (SAST) tool built with **Python** and **Streamlit**. Designed to bridge the gap between application development and security engineering, this tool scans Python source code for security vulnerabilities, dangerous coding patterns, hardcoded secrets, and unsafe execution functions before deployment.

With an intuitive dashboard interface inspired by modern security tools, developers can upload individual `.py` files or scan entire project workspaces to view actionable security metrics, interactive distribution charts, line-by-line vulnerability highlights, and automated secure code remediation suggestions.

---

## 📖 Table of Contents

- [📌 Description](#-description)
- [🎯 Purpose & Use Case](#-purpose--use-case)
- [🚀 Key Features](#-key-features)
- [💻 Requirements](#-requirements)
- [⚙️ Installation & Setup](#️-installation--setup)
- [📁 Project File Structure](#-project-file-structure)
- [📊 DFD Diagram](#-dfd-diagram)
- [🗂️ ER Diagram](#️-er-diagram)
- [⚠️ Known Bugs & Security Considerations](#️-known-bugs--security-considerations)
- [⚖️ Pros & Cons](#️-pros--cons)
- [🛑 Limitations](#-limitations)
- [🔮 Future Roadmap](#-future-roadmap)
- [🤝 Contributing](#-contributing)
- [⭐ Thanks & Support](#-thanks--support)

---

## 🎯 Purpose & Use Case

### Purpose
The primary purpose of this project is to democratize security analysis for developers, allowing them to shift security left in the Software Development Life Cycle (SDLC). 

### Primary Use Cases
1. **Pre-commit Code Reviews**: Analyze new Python files or functions locally before pushing to remote repositories.
2. **Educational Security Audit**: Help beginner to intermediate Python developers learn secure coding practices through direct side-by-side remediation examples.
3. **Quick Security Audits**: Generate instant security assessment reports for lightweight Python backend applications and microservices.

---

## 🚀 Key Features

- **🔍 Dynamic Rule Engine**: Detects dangerous patterns including Command Injection (`subprocess`, `os.system`), Code Execution (`eval`, `exec`), Hardcoded API Keys/Passwords, Flask Debug mode vulnerabilities, and Weak Cryptographic Hashing.
- **📊 Real-time Security Dashboard**: Displays live metric cards categorizing findings by severity (`Critical`, `High`, `Medium`, `Low`).
- **📈 Interactive Data Visualizations**: Automatically generates severity distribution charts and category breakdowns using Pandas and Streamlit charts.
- **📝 Live Code Editor**: Interactive code area allowing real-time editing and instant re-scanning without restarting the application.
- **💡 Vulnerability & Remediation Inspector**: Click any flagged issue line to view the vulnerable code snippet alongside a safe, copy-pasteable code replacement.
- **📥 Exportable Security Reports**: Download complete markdown security audit reports summarizing overall findings and recommendations.

---

## 💻 Requirements

Before setting up the application, ensure your environment meets the following requirements:

- **Python**: `3.8` or higher
- **Package Manager**: `pip` (Python package installer)
- **Dependencies**:
  - `streamlit >= 1.28.0`
  - `pandas >= 2.0.0`

---

## ⚙️ Installation & Setup

Follow these steps to set up and run the scanner on your local machine:

### 1. Clone the Repository
```bash
git clone https://github.com/alok--kumar8765/ai-code-security-scanner.git
cd ai-code-security-scanner
```

### 2. Create and Activate a Virtual Environment (Recommended)
- **Linux/macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
- **Windows:**
  ```cmd
  python -m venv venv
  venv\Scripts\activate
  ```

### 3. Install Required Dependencies
```bash
pip install streamlit pandas
```

### 4. Run the Streamlit Application
```bash
streamlit run app.py
```
After executing the command, Streamlit will open the application interface automatically in your browser at `http://localhost:8501`.

---

## 📁 Project File Structure

```text
ai-code-security-scanner/
│
├── app.py                      # Main Streamlit dashboard application
├── README.md                   # Comprehensive project documentation
└── requirements.txt            # Python dependencies package list
```

---

## 📊 DFD Diagram

### Data Flow Diagram (Level 1)

```text
  [ User / Developer ]
           │
           │ 1. Uploads .py File / Edits Code
           ▼
┌──────────────────────────────────────────────┐
│        Streamlit Dashboard Interface         │
└──────────────────────┬───────────────────────┘
                       │
                       │ 2. Sends Source String
                       ▼
┌──────────────────────────────────────────────┐
│           Security Scanning Engine           │
│        (AST & Pattern Matching Rules)        │
└──────────────────────┬───────────────────────┘
                       │
                       │ 3. Generates Structured Findings
                       ▼
┌──────────────────────────────────────────────┐
│            Session State Data Store          │
└──────────────┬────────────────┬──────────────┘
               │                │
 4. Renders UI │                │ 5. Compiles File
               ▼                ▼
┌──────────────────────┐┌──────────────────────┐
│ Charts & Inspector   ││  Markdown Report     │
│ Dashboard Visuals    ││  Download Generator  │
└──────────────────────┘└──────────────────────┘
```

---

## 🗂️ ER Diagram

### Entity-Relationship Diagram (Conceptual Schema)

```text
┌─────────────────────────┐          ┌─────────────────────────┐
│       SOURCE_FILE       │          │      VULNERABILITY      │
├─────────────────────────┤          ├─────────────────────────┤
│ PK  filename (String)   │ 1     N  │ PK  id (Integer)        │
│     content (Text)      ├─────────<│ FK  file (String)       │
│     line_count (Int)    │          │     severity (String)   │
└─────────────────────────┘          │     issue_type (String) │
                                     │     line (Integer)      │
                                     │     vulnerable_code     │
                                     │     recommendation      │
                                     │     secure_code         │
                                     └─────────────────────────┘
```

---

## ⚠️ Known Bugs & Security Considerations

### Known Bugs
- **Large File Performance**: Processing extremely large Python files (>10,000 lines) within the single-line regex scanner may temporarily degrade Streamlit UI performance.
- **Multiline String False Positives**: Static regular expressions may flag rule matches inside code comments or multiline string docstrings.

### Security Considerations
- This scanner runs locally on client equipment and does not send source code to external servers or third-party API providers.

---

## ⚖️ Pros & Cons

### Pros
- ⚡ **Zero-Configuration Execution**: Instant deployment via standard Streamlit server execution.
- 🎨 **Clear Visual Insights**: Graphical severity metrics and breakdown graphs for quick triage.
- 💡 **Actionable Fix Guidance**: Provides copy-pasteable secure replacements rather than raw error output.

### Cons
- 🔎 **Static Limits**: Uses static regex matching rather than complete dynamic execution or full AST taint-analysis.
- 🐍 **Language-Specific**: Currently limited exclusively to Python source files (`.py`).

---

## 🛑 Limitations

1. **Lack of Deep Taint Analysis**: Cannot trace variable origins dynamically across complex functions or multi-file dependencies.
2. **Framework Restrictions**: Rules currently target core Python standard library functions, Flask, and basic SQL/Crypto patterns. Heavy frameworks (Django, FastAPI) require customized rule additions.

---

## 🔮 Future Roadmap

- [ ] **AST Deep Parsing Integration**: Upgrade regex engine to Python standard `ast` parsing for reduced false positives.
- [ ] **Multi-Language Support**: Extend scanning capabilities to JavaScript, TypeScript, and Go files.
- [ ] **AI-Powered Code Remediation**: Integrate Large Language Models (LLMs) to automatically rewrite complex vulnerable functions.
- [ ] **CI/CD Pipeline Integration**: Provide a headless CLI module for GitHub Actions integration.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. **Fork** the Repository.
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`).
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`).
4. **Push** to the branch (`git checkout -b feature/AmazingFeature`).
5. **Open** a Pull Request.

---

## ⭐ Thanks & Support

If you find this project useful or helpful for learning application security practices, please consider leaving a **Star ⭐** on the repository!

Created with ❤️ by [alok--kumar8765](https://github.com/alok--kumar8765)