# 💼 Small Business ERP Lite

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B.svg)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458.svg)
![SQLite/MySQL](https://img.shields.io/badge/Database-SQLite%2FMySQL-003545.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Build](https://img.shields.io/badge/Build-Passing-brightgreen.svg)

> What if you could manage your entire small business from a single interactive dashboard?  
> **Small Business ERP Lite** is an all-in-one business management application designed to simplify inventory management, sales tracking, customer relationships, and real-time business analytics.

---

## 📐 Table of Contents

- [📌 Purpose & Use Case](#-purpose--use-case)
- [✨ Features](#-features)
- [🎨 Multi-Theme Support](#-multi-theme-support)
- [📦 Requirements](#-requirements)
- [🚀 Installation & Setup](#-installation--setup)
- [📂 File Structure](#-file-structure)
- [📊 Data Flow Diagram (DFD)](#-data-flow-diagram-dfd)
- [🗄️ Entity Relationship (ER) Diagram](#%EF%B8%8F-entity-relationship-er-diagram)
- [⚖️ Pros & Cons](#%EF%B8%8F-pros--cons)
- [⚠️ Limitations](#%EF%B8%8F-limitations)
- [🔒 Bugs & Vulnerabilities](#-bugs--vulnerabilities)
- [🔮 Future Updates](#-future-updates)
- [🤝 Contributing](#-contributing)
- [⭐ Thanks & Support](#-thanks--support)
- [🌈 Creator & Copyright](#-creator--copyright)

---

## 📌 Purpose & Use Case

Small businesses frequently struggle with fragmented tools—relying on manual spreadsheets for inventory, paper logs for sales, and unconnected tools for customer tracking.

**Small Business ERP Lite** unifies essential operational tasks into a single dashboard. Designed for retail shop owners, wholesalers, and small enterprises, it gives managers immediate visual control over stock levels, low-stock reorder alerts, customer logs, revenue performance metrics, and sales trend analytics.

---

## ✨ Features

- **📦 Inventory Management:** Add, track, filter, and monitor stock quantities and unit pricing.
- **⚠️ Low Stock Alerts:** Automated detection and visual warning table for products at or below safety reorder levels.
- **🛍️ Sales & Order Tracking:** Record sales, calculate totals automatically, and adjust inventory quantities in real time.
- **👥 Customer Directory:** Maintain customer profiles, order associations, and contact details.
- **📊 Real-Time Analytics:** Dynamic visual revenue trend lines and stock level bar charts powered by Pandas and Streamlit.
- **🎨 Dynamic Multi-Theme Engine:** Toggle live between **Modern Dark**, **Light Clean**, and **Cyberpunk** visual interfaces.

---

## 🎨 Multi-Theme Support

The application includes an integrated CSS theme parser allowing dynamic style switching:

| Theme Name | Background | Primary Accent | Best Environment |
| :--- | :--- | :--- | :--- |
| **Modern Dark** | `#12121c` | `#6c5ce7` | Night ops & low-light usage |
| **Light Clean** | `#f4f7f6` | `#3498db` | Standard office environment |
| **Cyberpunk** | `#0b0514` | `#ff007f` | High-contrast neon interface |

---

## 📦 Requirements

- **Python Version:** Python `3.8+`
- **Dependencies:**
  - `streamlit >= 1.28.0`
  - `pandas >= 2.0.0`
  - `sqlite3` (Included in standard Python library)

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/alok--kumar8765/small-business-erp-lite.git
cd small-business-erp-lite
```

### 2. Create & Activate Virtual Environment
```bash
# On Windows
python -m venv env
env\Scripts\activate

# On macOS/Linux
python3 -m venv env
source env/bin/activate
```

### 3. Install Dependencies
```bash
pip install streamlit pandas
```

### 4. Run the Application
```bash
streamlit run app.py
```
*The app will launch automatically in your web browser at `http://localhost:8501`.*

---

## 📂 File Structure

```
small-business-erp-lite/
├── app.py              # Main single-file Streamlit application logic
├── erp_lite.db         # SQLite database file (Auto-generated on startup)
├── requirements.txt    # Python dependencies file
└── README.md           # Documentation
```

---

## 📊 Data Flow Diagram (DFD)

```
                       +-------------------------+
                       |    Business Manager     |
                       +-------------------------+
                                    |
                                    | (Form Inputs: Sales, Products, Customers)
                                    v
                       +-------------------------+
                       |   1.0 Streamlit UI      |
                       |      Control Layer      |
                       +-------------------------+
                                    |
                 +------------------+------------------+
                 |                                     |
                 v                                     v
     +-----------------------+             +-----------------------+
     |  2.0 Transaction      |             |  3.0 Analytics        |
     |      Processor        |             |      Engine (Pandas)  |
     +-----------------------+             +-----------------------+
                 |                                     |
                 | (SQL Writes / Updates)              | (SQL Aggregations)
                 v                                     v
     +-------------------------------------------------------------+
     |                     4.0 Database Store                      |
     |             (Tables: Inventory, Sales, Customers)           |
     +-------------------------------------------------------------+
```

---

## 🗄️ Entity Relationship (ER) Diagram

```
 +---------------------+           1         N           +---------------------+
 |      CUSTOMERS      | -------------------------------- |        SALES        |
 +---------------------+                                 +---------------------+
 | customer_id (PK)    |                                 | sale_id (PK)        |
 | name                |                                 | customer_name (FK)  |
 | email               |                                 | item_name (FK)      |
 | phone               |                                 | quantity            |
 +---------------------+                                 | total_price         |
                                                         | date                |
                                                         +---------------------+
                                                                    | N
                                                                    |
                                                                    | 1
                                                         +---------------------+
                                                         |      INVENTORY      |
                                                         +---------------------+
                                                         | item_id (PK)        |
                                                         | item_name           |
                                                         | category            |
                                                         | quantity            |
                                                         | min_stock           |
                                                         | price               |
                                                         +---------------------+
```

---

## ⚖️ Pros & Cons

| Pros 🟢 | Cons 🔴 |
| :--- | :--- |
| **Zero Setup Database:** Auto-initializes SQLite database with sample data. | **Single-User Concurrent Limits:** SQLite handles low concurrency compared to client-server MySQL. |
| **Real-Time Visuals:** Immediate metric card & chart refreshes on state change. | **Browser Dependency:** Operates inside web browsers rather than native desktop wrappers. |
| **Multi-Theme Engine:** Flexible CSS color schemes. | **No Native Mobile APK:** Accessible via mobile browsers, but lacks native mobile builds. |

---

## ⚠️ Limitations

1. **Local Network Context:** Built for single-store or small local office deployment.
2. **Thermal Receipt Driver:** Does not communicate directly with USB serial receipt printers out-of-the-box.

---

## 🔒 Bugs & Vulnerabilities

- **Concurrent Write Locking:** High simultaneous database transactions can trigger standard SQLite busy locks.
- **Input Sanitization:** Form entry fields rely on parameterized SQL queries; ensure any future SQL extensions maintain raw query parameters (`?`).

---

## 🔮 Future Updates

- [ ] **Barcode Reader:** Direct USB/Webcam barcode scan input for billing.
- [ ] **PDF Invoice Generator:** Downloadable branded receipt PDF generation.
- [ ] **Multi-Branch Support:** Multi-location stock allocation tracking.
- [ ] **Authentication System:** Multi-user role authorization (Admin vs. Cashier).

---

## 🤝 Contributing

Contributions are welcome!

1. Fork this Repository (`https://github.com/alok--kumar8765/small-business-erp-lite/fork`)
2. Create your Feature Branch (`git checkout -b feature/NewFeature`)
3. Commit your Changes (`git commit -m 'Add NewFeature'`)
4. Push to Branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

---

## ⭐ Thanks & Support

If this project helps streamline your workflow or project vision, please consider giving it a **⭐ Star** on GitHub!

Developed with ❤️ by [**alok--kumar8765**](https://github.com/alok--kumar8765).

---

<div align="center">
    <h3><span style="color:#ff3366;">Creator:</span> <span style="color:#ff9900;">Generative AI</span> | <span style="color:#3399ff;">Copyrights</span> <span style="color:#cc33ff;">2026</span></h3>
</div>