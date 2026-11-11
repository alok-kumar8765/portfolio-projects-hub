# 🌿 AgriDetect: Multi-Crop Disease Detection & Severity Analysis Engine

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.12%2B-FF6F00.svg)](https://tensorflow.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

AgriDetect is a production-ready, client-server agricultural diagnostic system designed to bridge the gap between advanced deep learning and field-level agronomy. Built around a high-performance FastAPI backend and a scalable CNN architecture (**EfficientNetB0**), the system ingests crop leaf images, executes multi-class disease classification across the PlantVillage taxonomy, calculates infection severity percentages using computer vision color-masking pipelines, and delivers actionable treatment and prevention advisories.

---

## 📑 Table of Contents
1. [Core Features](#-core-features)
2. [System Architecture](#-system-architecture)
3. [Project Structure](#-project-structure)
4. [Installation & Setup Guide](#-installation--setup-guide)
5. [Running the Application](#-running-the-application)
6. [API Usage & Integration](#-api-usage--integration)
7. [Pros & Cons](#-pros--cons)
8. [Limitations](#-limitations)
9. [Bugs & Vulnerabilities](#-bugs--vulnerabilities)
10. [Future Advancements](#-future-advancements)
11. [Contributing](#-contributing)
12. [License & Acknowledgments](#-license--acknowledgments)

---

## 🚀 Core Features
* **Multi-Crop Classification:** Detects health statuses and specific pathologies across multiple staple and cash crops (utilizing the PlantVillage dataset taxonomy).
* **Computer Vision Severity Scoring:** Automatically computes leaf damage ratios (`%` area affected) via OpenCV HSV color-space masking to evaluate infection urgency.
* **Tiered Field Advisory:** Dynamically maps disease metrics into actionable severity tiers (Low, Medium, High) paired with organic remedies and preventive strategies.
* **Decoupled Client-Server API:** Exposes a clean RESTful endpoint (`/predict`) designed for seamless integration with external clients (e.g., native Android mobile applications).
* **Interactive Diagnostic Dashboard:** Features a Streamlit-powered web UI for rapid prototyping, batch sample testing, and visual result verification.

---

## 🏗️ System Architecture


```

+------------------+      HTTP POST (Multipart)      +-----------------------------+
|   Android App /  | ------------------------------> | FastAPI Backend (Server)    |
|   Streamlit UI   | <------------------------------ | - OpenCV Severity Pipeline  |
+------------------+         JSON Response           | - EfficientNetB0 Classifier |
+-----------------------------+

```

---

## 📂 Project Structure
```text
Agricultural Crop Disease Detection/
│
├── main.py                # FastAPI backend server
├── app_ui.py              # Streamlit interactive dashboard
├── saved_crop_model.h5    # Trained EfficientNetB0 weights file
├── class_indices.json     # Dynamic class label mapping dictionary
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation

```

---

## 🛠️ Installation & Setup Guide

### 1. Prerequisites

Ensure you have **Python 3.11+** installed on your system.

### 2. Clone or Set Up Workspace

Navigate to your project directory in your terminal:

```bash
cd "C:\Users\AIT\Downloads\Agricultural Crop Disease Detection"

```

### 3. Create and Activate Virtual Environment

```bash
python -m venv .venv
source .venv/Scripts/activate   # On Windows Git Bash / UCRT64
# Or `.venv\Scripts\activate` for standard Windows Command Prompt

```

### 4. Install Dependencies

Create a `requirements.txt` file with the required libraries:

```text
fastapi
uvicorn
tensorflow
numpy
opencv-python
streamlit
requests
pillow
python-multipart

```

Install them via pip:

```bash
pip install -r requirements.txt

```

---

## 💻 Running the Application

Running the system requires two concurrent terminal windows (one for the backend API, one for the user interface).

### Step 1: Start the FastAPI Backend

```bash
uvicorn main:app --reload

```

* *Server will launch live at:* `http://127.0.0.1:8000`
* *Interactive API Docs:* `http://127.0.0.1:8000/docs`

### Step 2: Launch the Streamlit Dashboard (Optional Local UI)

Open a second terminal window, activate your virtual environment, and run:

```bash
python -m streamlit run app_ui.py

```

* *UI will launch automatically at:* `http://localhost:8501`

---

## 🔌 API Usage & Integration (For Android Developers)

The backend exposes a single RESTful endpoint designed to accept image byte streams via HTTP POST.

* **Endpoint URL:** `http://<YOUR_SERVER_IP>:8000/predict`
* **Method:** `POST`
* **Content-Type:** `multipart/form-data`
* **Form Parameter:** `file` (Binary image data)

### Example JSON Response Structure:

```json
{
  "status": "success",
  "prediction": "Tomato___Late_blight",
  "confidence": 96.42,
  "severity_percentage": 28.5,
  "severity_tier": "Medium",
  "recommendation": "Moderate spread. Apply approved bio-fungicides or copper-based sprays."
}

```

---

## ⚖️ Pros & Cons

### Pros

* **Decoupled Architecture:** Separation of concerns allows the AI model to scale on server hardware while lightweight clients (Android/Web) handle user presentation.
* **Extensible:** Adding new crops or diseases only requires retraining the model weights and updating label mappings without modifying routing logic.
* **Quantitative Metrics:** Goes beyond simple classification by calculating physical damage ratios via computer vision.

### Cons

* **Server Dependency:** Requires active network connectivity between the mobile client and the backend server to perform predictions.
* **Compute Overhead:** Running heavy CNN backbones (`EfficientNetB0`) and OpenCV pipelines on constrained server hardware can increase latency under high concurrent load.

---

## ⚠️ Limitations

* **Lighting Variations:** Extreme field lighting conditions (direct harsh sunlight, deep shadows) can occasionally interfere with OpenCV color-masking severity calculations.
* **Leaf Orientation:** Images with overlapping leaves or obscured focal points may reduce classification confidence.

---

## 🐛 Bugs & Vulnerabilities

* **Unvalidated Image Payloads:** Uploading non-image binary files or corrupted streams can trigger unhandled OpenCV buffer decoding errors if input validation fails. *(Mitigated in current builds via type-checking guards).*
* **Memory Spike Risk:** Processing high-resolution raw camera images concurrently without stream batching can cause temporary RAM spikes on low-tier servers.

---

## 🔮 Future Advancements

* **Edge Deployment (TFLite):** Bundle lightweight quantized models directly into the Android application for offline, remote-field farming support without internet dependency.
* **Database Integration:** Connect FastAPI to a persistent PostgreSQL database to track historical field scans, farmer profiles, and regional disease outbreaks over time.
* **Multilingual Support:** Integrate regional Indian language translation layers (Hindi, Telugu, Marathi, Tamil) directly into the API response schema.

---

## 👥 Contributing

Contributions, bug reports, and feature requests are welcome! Feel free to open an issue or submit a pull request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git origin push feature/AmazingFeature`)
5. Open a Pull Request

---

## ⭐ License

Distributed under the MIT License. See `LICENSE` for more information.
