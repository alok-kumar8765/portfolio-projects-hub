# 📊 Enterprise Sales Forecasting & Analytics System

An enterprise-grade, machine-learning-driven sales forecasting and analytics dashboard built using **Python**, **Streamlit**, **Scikit-learn**, and **Plotly**. 

This system dynamically inspects uploaded datasets (CSV/Excel), infers field types, executes recursive multi-step temporal predictions with 95% confidence intervals, and presents an interactive executive analytics dashboard.

---

## 🛡️ Badges

![Python Version](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.32.0+-red.svg)
![Machine Learning](https://img.shields.io/badge/Scikit--Learn-Random%20Forest-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![GitHub Stars](https://img.shields.io/github/stars/alok-kumar8765/sales-forecasting-system?style=social)
![GitHub Forks](https://img.shields.io/github/forks/alok-kumar8765/sales-forecasting-system?style=social)

---

## 📌 Table of Contents

- [Description](#-description)
- [Key Features](#-key-features)
- [System Architecture & Design](#-system-architecture--design)
  - [Architecture Diagram](#architecture-diagram)
  - [Data Flow Diagram (DFD)](#data-flow-diagram-dfd)
  - [Entity-Relationship (ER) Diagram](#entity-relationship-er-diagram)
- [Folder Structure](#-folder-structure)
- [Requirements & Dependencies](#-requirements--dependencies)
- [Installation & Setup Guide](#-installation--setup-guide)
- [User Guide](#-user-guide)
  - [Who Can Use This System?](#who-can-use-this-system)
  - [How to Use the Application](#how-to-use-the-application)
- [Pros & Cons](#-pros--cons)
- [Current Limitations](#-current-limitations)
- [Future Roadmap & Updates](#-future-roadmap--updates)
- [Contributing](#-contributing)
- [License & Acknowledgments](#-license--acknowledgments)

---

## 📖 Description

Predicting enterprise demand and managing inventory levels requires balancing historical trend analysis, temporal autocorrelation, and uncertainty management. Standard off-the-shelf desktop applications freeze during heavy ML operations and often fail when input schema definitions vary.

The **Enterprise Sales Forecasting & Analytics System** addresses these issues by offering:
1. **Schema Agnosticism:** Dynamic dropdown mapping allows users to upload raw sales datasets without adhering to rigid column-naming conventions.
2. **Recursive Multi-Step Forecasting:** Generates 30, 60, or 90-day future horizons using auto-regressive lag ($t-1, t-7, t-30$) and rolling average features.
3. **Statistical Uncertainty Modeling:** Computes residual standard errors to generate upper and lower 95% confidence bounds around forecasts.
4. **Performance Optimization:** Implements Streamlit data caching (`@st.cache_data`) to prevent model retraining during UI interactions.

---

## ✨ Key Features

- 📂 **Schema-Agnostic Ingestion:** Compatible with both `.csv` and `.xlsx` files. Automatic feature detection isolates dates, metrics, and categories.
- ⚙️ **Automated Resampling & Cleaning:** Converts timestamp series into continuous daily intervals (`.asfreq('D')`), replacing missing values through forward-filling algorithms.
- 🌲 **Recursive Random Forest Predictor:** Trains on historical lag patterns and calendar metadata (day of week, month, quarter).
- 📉 **95% Confidence Interval Calculation:** Projects fan-shaped error bounds ($\pm 1.96 \times \sigma_{\text{residuals}} \times \sqrt{t}$) as the forecast horizon extends.
- 📊 **Executive Analytics Suite:** Interactive Plotly charts including trend line plots with uncertainty bands, day-of-week bar charts, and category donut distributions.
- 📥 **Export-Ready Output:** One-click CSV export of forecasted values alongside upper and lower risk thresholds.

---

## 📐 System Architecture & Design

### Architecture Diagram

```
+-----------------------------------------------------------------+
|                      USER INTERFACE (Streamlit)                 |
|  [ File Upload ] -> [ Column Mapper ] -> [ Interactive Charts ] |
+--------------------------------+--------------------------------+
                                 |
                                 v
+-----------------------------------------------------------------+
|                      CONTROLLER & DATA PIPELINE                 |
|   - Pandas: Format Parsing, Type Coercion, Resampling           |
|   - Validation: NaN Drop, Chronological Sorting                 |
+--------------------------------+--------------------------------+
                                 |
                                 v
+-----------------------------------------------------------------+
|                      MACHINE LEARNING CORE                      |
|   - Feature Engineering (Lags: 1, 7, 30 | Rolling: 7, 30)      |
|   - Model: Scikit-Learn RandomForestRegressor                   |
|   - Residual Analysis & Confidence Bound Calculation            |
+-----------------------------------------------------------------+
```

### Data Flow Diagram (DFD)

```
[User CSV/XLSX] ---> (1. Data Ingestion & Schema Mapping)
                              |
                              v
                   (2. Daily Resampling & Cleaning)
                              |
                              v
                   (3. Feature Engineering Engine)
                       (Lags & Calendar Features)
                              |
                              v
                   (4. Random Forest Model Training) <--- [Cached Model]
                              |
                              v
                   (5. Recursive Horizon Predictor)
                              |
                              v
                   (6. Plotly Interactive Dashboard & CSV Exporter)
```

### Entity-Relationship (ER) Diagram

```
+--------------------+        +-------------------------+
|   Raw Data Input   |        |   Resampled Daily Data  |
+--------------------+        +-------------------------+
| PK  Record_ID      | 1    N | PK  Date                |
|     Timestamp      |------->|     Aggregated_Sales    |
|     Sales_Amount   |        |     Day_of_Week         |
|     Category (Opt) |        |     Quarter             |
+--------------------+        +-------------------------+
                                           |
                                           | 1
                                           |
                                           v 1
                              +-------------------------+
                              |   Model Features        |
                              +-------------------------+
                              | PK  Date                |
                              | FK  Aggregated_Sales    |
                              |     Lag_1, Lag_7, Lag_30|
                              |     Rolling_Mean_7, 30  |
                              +-------------------------+
                                           |
                                           | 1
                                           |
                                           v 1..N
                              +-------------------------+
                              |   Forecast Output       |
                              +-------------------------+
                              | PK  Forecast_Date       |
                              |     Predicted_Sales     |
                              |     Lower_Bound_95      |
                              |     Upper_Bound_95      |
                              +-------------------------+
```

---

## 📁 Folder Structure

```
sales-forecasting-system/
├── app.py                      # Main Streamlit Dashboard Application
├── requirements.txt            # Python Dependencies
├── README.md                   # Project Documentation
├── dummy_sales_data.csv        # Sample Dataset for Testing
└── .streamlit/
    └── config.toml             # Custom UI Theme Configuration (Optional)
```

---

## 📋 Requirements & Dependencies

- **Python:** Version `3.9` or higher
- **Core Libraries:**
  - `streamlit>=1.32.0`
  - `pandas>=2.0.0`
  - `numpy>=1.24.0`
  - `scikit-learn>=1.3.0`
  - `plotly>=5.18.0`
  - `openpyxl>=3.1.0` (for Excel parsing)

---

## 🚀 Installation & Setup Guide

### 1. Clone the Repository
```bash
git clone https://github.com/alok-kumar8765/sales-forecasting-system.git
cd sales-forecasting-system
```

### 2. Create and Activate a Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run app.py
```
The application will launch automatically in your default browser at `http://localhost:8501`.

---

## 💡 User Guide

### Who Can Use This System?

- **Retail Operations Managers:** To forecast stock demands and mitigate overstock or stockout scenarios.
- **Financial Analysts:** To project rolling revenue metrics over 30/60/90-day time horizons.
- **Supply Chain Planners:** To align procurement schedules with seasonal patterns and trend fluctuations.
- **Data Scientists & Developers:** As a modular reference architecture for building interactive Streamlit ML apps.

### How to Use the Application

1. **Upload Dataset:** Expand the left sidebar and click **Upload CSV or Excel File**.
2. **Configure Mappings:**
   - Select your dataset's **Date/Timestamp** column.
   - Select your dataset's **Numeric Target Sales** column.
   - (Optional) Select a **Categorical** column for store/product breakdowns.
   - Choose a **Forecast Horizon** (30, 60, or 90 days).
3. **Inspect Insights:**
   - Review **MAPE** and **RMSE** error metrics in the top dashboard.
   - Analyze predicted trends along with the shaded 95% Confidence Interval band.
   - Examine day-of-week sales patterns and category breakdowns.
4. **Export Results:** Scroll to the bottom table and click **Download Forecast CSV**.

---

## ⚖️ Pros & Cons

### Pros
- ⚡ **Highly Responsive:** Built on Streamlit with `@st.cache_data` logic for responsive performance.
- 🛠️ **Format Flexible:** Ingests unformatted raw logs or aggregated daily files without requiring pre-cleaning.
- 🎯 **Risk-Aware:** Quantifies forecast uncertainty using expanding confidence limits over long prediction windows.
- 📊 **Rich Visuals:** Powered by interactive Plotly graphics rather than static charts.

### Cons
- 🌲 **Tree Extrapolation Limit:** Standard tree ensembles cannot project linear trends far beyond historical maximums.
- 🗓️ **External Factor Ignorance:** Current models do not incorporate external economic indicators or marketing spend metrics.

---

## 🛑 Current Limitations

1. **Data Density Requirements:** The pipeline requires at least **60 continuous days** of daily history to build lag features (`lag_30`, `rolling_mean_30`).
2. **Single Target Modeling:** Forecasts total aggregate sales; individual multi-item forecasting requires filtering the dataset per run.

---

## 🔮 Future Roadmap & Updates

- [ ] **Prophet & LightGBM Integration:** Allow users to toggle between Random Forest, Facebook Prophet, and LightGBM models.
- [ ] **Automated Holiday Mapping:** Automatically integrate country-specific holiday calendars into feature generation.
- [ ] **Multi-Item Batch Forecasting:** Provide automated batch processing to predict multiple SKUs simultaneously.
- [ ] **Dockerization & CI/CD Pipeline:** Package the system in a lightweight Docker container with automated GitHub Actions testing.

---

## 🤝 Contributing

Contributions are welcome! Follow these steps to contribute:

1. **Fork the Repository**
2. **Create a Feature Branch:** `git checkout -b feature/AmazingFeature`
3. **Commit Your Changes:** `git commit -m 'Add some AmazingFeature'`
4. **Push to the Branch:** `git push origin feature/AmazingFeature`
5. **Open a Pull Request**

---

## 🌟 Show Your Support

If you find this project useful, please consider giving it a **Star** on GitHub!

Developed with ❤️ by **[Alok Kumar](https://github.com/alok-kumar8765)**.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more details.