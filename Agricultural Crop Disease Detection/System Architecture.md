Here is the complete architectural blueprint, system design, data flow diagram (DFD), entity-relationship (ER) structure, and production folder layout updated for your GitHub repository (`alok-kumar8765`). You can append or integrate these sections directly into your `README.md`.

---

## 📥 Cloning Repository

To clone this project directly from your GitHub profile:

```bash
git clone https://github.com/alok-kumar8765/Agricultural-Crop-Disease-Detection.git
cd Agricultural-Crop-Disease-Detection

```

---

## 📂 Complete Project Folder Structure

```text
Agricultural-Crop-Disease-Detection/
│
├── .gitignore
├── README.md                      # Comprehensive project documentation
├── requirements.txt               # Python package dependencies
│
├── backend/                       # Core Server & AI Logic
│   ├── main.py                    # FastAPI application & endpoints
│   ├── saved_crop_model.h5        # Trained EfficientNetB0 model weights
│   └── class_indices.json         # Dynamic class label mappings
│
├── frontend_web/                  # Prototyping & Testing Dashboard
│   └── app_ui.py                  # Streamlit interactive UI
│
├── pipeline/                      # Computer Vision & Data Utilities
│   ├── severity_analyzer.py       # OpenCV HSV color-masking damage calculator
│   └── preprocess.py              # Image normalization & tensor conversion
│
└── dataset/                       # Local/Cloud Dataset Reference
    └── data_distribution_for_SVM/ # Pre-split train & validation folders

```

---

## 🏛️ System Design & Architecture

The system follows a **Decoupled Client-Server RESTful Architecture**. The heavy compute tasks (Deep Learning inference and computer vision pixel calculations) are isolated on a backend server or PC, allowing lightweight mobile clients (Android) or web dashboards to interact seamlessly over HTTP.

```
+--------------------+        HTTP POST        +-----------------------------------+
|  Android Client /  |  (Multipart Image Payload) |         FastAPI Backend           |
|   Streamlit Web    | ----------------------> | - Input Validation & Stream Read  |
|     Dashboard      |                         | - OpenCV HSV Severity Pipeline    |
|                    | <---------------------- | - TensorFlow EfficientNetB0 Model |
+--------------------+      JSON Response      +-----------------------------------+

```

---

## ⚙️ End-to-End Execution Pipeline

1. **Image Capture / Selection:** The user snaps a photo via the Android app camera or uploads a leaf sample through the Streamlit web dashboard.
2. **Payload Transmission:** The client packages the image bytes into a multipart form-data HTTP POST request and transmits it to the FastAPI endpoint (`/predict`).
3. **OpenCV Severity Analysis:** The backend decodes the image matrix, transforms it to the HSV color space, applies green-spectrum masking to isolate the leaf, and computes the ratio of diseased/necrotic pixels to total leaf pixels to derive the **Severity Percentage**.
4. **Deep Learning Inference:** The image is resized to `224x224`, normalized, and passed through the pre-trained `EfficientNetB0` model to classify the exact disease category with a confidence score.
5. **Advisory Mapping:** The predicted class and computed severity score are mapped against structured agronomic databases to retrieve tailored organic remedies and preventative protocols.
6. **JSON Response Delivery:** A structured JSON payload is returned to the client for immediate rendering.

---

## 📊 Data Flow Diagram (DFD)

### Level 0 DFD (Context Diagram)

```
  [ Farmer / User ] 
         │
         │ Leaf Image (Multipart)
         ▼
┌─────────────────────────────────┐
│     AgriDetect FastAPI System   │
└─────────────────────────────────┘
         │
         │ JSON (Prediction, Severity %, Remedial Action)
         ▼
  [ Mobile App / Dashboard UI ]

```

### Level 1 DFD (Process Breakdown)

```
[Client Image] ──► (1.0 Image Ingestion & Decode) ──► Raw BGR Matrix
                         │
                         ├──────────────────────────────────┐
                         ▼                                  ▼
           (2.0 OpenCV Severity Engine)          (3.0 TF Model Inference)
           - HSV Color Space Masking             - Resize & Normalization
           - Pixel Damage Ratio Calc             - EfficientNetB0 Forward Pass
                         │                                  │
                         ▼                                  ▼
                 [ Severity % & Tier ]               [ Predicted Class ID & Confidence ]
                         │                                  │
                         └────────────────┬─────────────────┘
                                          ▼
                         (4.0 Advisory Mapping & Response Builder)
                                          │
                                          ▼
                                   [ JSON Payload ]

```

---

## 🗄️ Entity-Relationship (ER) Design

If you scale this project to persist history in a relational database (e.g., PostgreSQL), the logical data model consists of these core entities:

```
+-------------------+       1:N       +-------------------+       1:1       +--------------------+
|     Farmer /      | ──────────────► |  PredictionLog    | ──────────────► |  TreatmentAdvisory |
|     User          |                 |                   |                 |                    |
+-------------------+                 +-------------------+                 +--------------------+
| - user_id (PK)    |                 | - log_id (PK)     |                 | - advisory_id (PK) |
| - phone_number    |                 | - user_id (FK)    |                 | - disease_name     |
| - region          |                 | - image_url       |                 | - severity_tier    |
+-------------------+                 | - predicted_class |                 | - organic_remedy   |
                                      | - confidence_score|                 | - prevention_steps |
                                      | - severity_pct    |                 +--------------------+
                                      | - timestamp       |
                                      +-------------------+

```