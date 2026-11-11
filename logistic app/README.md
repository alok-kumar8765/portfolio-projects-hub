# 🚛 Generative AI Logistics Enterprise Suite

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-red.svg)](https://streamlit.io/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey.svg)](https://www.sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub owner](https://img.shields.io/badge/GitHub-alok--kumar8765-blueviolet)](https://github.com/alok--kumar8765)

---

## 📋 Table of Contents
1. [Use & Purpose](#-use--purpose)
2. [Features](#-features)
3. [Requirements](#-requirements)
4. [Installation & Setup](#-installation--setup)
5. [API Keys Note](#-api-keys-note)
6. [File Structure](#-file-structure)
7. [System Architecture: Data Flow Diagram (DFD)](#-system-architecture-data-flow-diagram-dfd)
8. [Database Schema: ER Diagram](#-database-schema-er-diagram)
9. [Pros & Cons](#-pros--cons)
10. [Limitations](#-limitations)
11. [Bugs & Vulnerabilities](#-bugs--vulnerabilities)
12. [Future Updates](#-future-updates)
13. [Contributing, Star & Thanks](#-contributing-star--thanks)

---

## 🎯 Use & Purpose
The **Generative AI Logistics Enterprise Suite** is an all-in-one operations management dashboard built to bridge the gap between real-time spatial telemetry, supply chain tracking, financial invoicing, and multi-role enterprise workflows. 

Its primary purpose is to empower logistics CEOs, dispatchers, drivers, and corporate clients with a centralized web-based platform to manage shipments, track truck fuel/capacities, monitor IoT engine/brake telemetry, generate automated billing invoices, and facilitate secure communications without relying on complex, bloated enterprise stacks.

---

## ✨ Features
* **Role-Based Access Control (RBAC):** Secure login portal mapping users dynamically into three dedicated views: **Admin/CEO** (full suite access), **Driver Portal** (assigned routes), and **Client Portal** (invoice history & order tracking).
* **Live Fleet Interactive Map:** Built with `Folium` and `streamlit-folium`, displaying real-time geographic vehicle coordinates over a dark-mode spatial grid.
* **Automated PDF Invoicing & Bill of Lading (BOL):** Instant generation and downloading of PDF invoices when a delivery status is marked as *Completed*.
* **Predictive Maintenance & IoT Telemetry:** Real-time sensor indicators tracking truck mileage, engine temperatures, and brake pad wear to forecast maintenance needs.
* **Internal Dispatcher-Driver Chat Webhook:** Real-time messaging drawer for transmitting urgent road notes between headquarters and specific vehicle units.
* **Dynamic Database Management:** Full CRUD (Create, Read, Update, Delete) capability across shipments, clients, drivers, trucks, and historical audit logs via SQLite.

---

## 📦 Requirements
* Python 3.9 or higher
* Streamlit
* Pandas
* Matplotlib
* Folium
* Streamlit-Folium
* FPDF2 (fpdf)

---

## ⚙️ Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/alok--kumar8765/logistic-app.git](https://github.com/alok--kumar8765/logistic-app.git)
   cd logistic-app

```

2. **Create & Activate a Virtual Environment:**
```bash
python -m venv env
# On Windows:
env\Scripts\activate
# On macOS/Linux:
source env/bin/activate

```


3. **Install Dependencies:**
```bash
pip install streamlit pandas matplotlib folium streamlit-folium fpdf2

```


4. **Run the Application:**
```bash
streamlit run app.py

```



---

## 🔑 API Keys Note

* **No paid API keys are strictly required** to run this application out-of-the-box.
* The interactive map utilizes open-source CartoDB dark tiles via `Folium`, meaning it loads instantly without needing a Mapbox or Google Maps API key.

---

## 🗂 File Structure

```text
logistic-app/
│
├── app.py                 # Main Streamlit application entry point
├── logistics.db           # Embedded SQLite relational database (auto-generated)
├── requirements.txt       # Project dependencies list
└── README.md              # Project documentation

```

---

## 📊 System Architecture: Data Flow Diagram (DFD)

```text
[ User Login ] ---> ( RBAC Security Engine )
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
   [ Admin / CEO ]   [ Driver Portal ]  [ Client Portal ]
        │                │                │
        ├────────────────┴────────────────┤
        ▼                                 ▼
 [ SQLite Database ] <---> [ Streamlit UI Components & Charts ]
        │
        ├---> (Triggers PDF Invoice Generation on Status = 'Completed')
        ├---> (Updates IoT Fleet Telemetry & Maintenance Alerts)
        └---> (Syncs Dispatcher-Driver Chat Webhook Logs)

```

---

## 📐 Database Schema: ER Diagram

```text
┌────────────────────────┐       ┌────────────────────────┐
│       SHIPS            │       │        DRIVERS         │
├────────────────────────┤       ├────────────────────────┤
│ PK  id                 │       │ PK  id                 │
│     driver_name        │       │     driver_name        │
│     truck_id           │       │     license_no         │
│     shipment_code      │       │     phone              │
│     status             │       │     assigned_truck     │
│     amount             │       │     rating             │
└────────────────────────┘       └────────────────────────┘
         │                                   │
         │ (Maps via Truck/Driver ID)        │
         ▼                                   ▼
┌────────────────────────┐       ┌────────────────────────┤
│        TRUCKS          │       │        CLIENTS         │
├────────────────────────┤       ├────────────────────────┤
│ PK  id                 │       │ PK  id                 │
│     truck_code         │       │     company_name       │
│     model              │       │     contact_person     │
│     max_capacity_t     │       │     email              │
│     mileage_km         │       │     total_volume       │
│     engine_temp_c      │       └────────────────────────┘
└────────────────────────┘

```

---

## ⚖️ Pros & Cons

### **Pros:**

* Highly responsive web interface powered by Streamlit.
* Zero external cloud dependencies (runs locally on a single embedded SQLite database file).
* Comprehensive business coverage (Operations + Finance + IoT + HR/Personnel).

### **Cons:**

* Local SQLite file locking can limit concurrent write operations under heavy multi-user enterprise traffic.
* Limited native styling customization compared to a custom React/Tailwind frontend.

---

## 🛑 Limitations

* Real-time GPS location tracking is simulated through static coordinates on the map rather than live cellular/telematics hardware polling.
* Chat webhook functions via database persistence rather than live WebSockets, requiring manual page refreshes or widget re-runs to pull incoming messages.

---

## 🐛 Bugs & Vulnerabilities

* **Authentication Security:** The current prototype stores administrator credentials inside a local SQLite table in plain text; production deployment requires secure hashing (e.g., bcrypt).
* **Concurrent SQLite Writes:** Rapid multi-user edits on the `data_editor` components may occasionally raise database lock exceptions if concurrent transactions collide.

---

## 🚀 Future Updates

* [ ] Migrate backend database connection pool from SQLite to PostgreSQL.
* [ ] Implement secure password hashing (bcrypt) and JSON Web Token (JWT) session cookies.
* [ ] Integrate true WebSocket-based live chat messaging.
* [ ] Add automated email dispatching for generated PDF invoices via SMTP/SendGrid.

---

## ⭐ Contributing, Star & Thanks

### **Contribute**

Contributions, bug reports, and feature requests are welcome! Feel free to fork this repository and submit pull requests to `alok--kumar8765`.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git origin push feature/AmazingFeature`)
5. Open a Pull Request

### **Star the Repo**

If you found this project helpful or inspiring, please give it a ⭐️ on GitHub!

### **Special Thanks**

Developed with ❤️ by **[Alok Kumar](https://www.google.com/url?sa=E&source=gmail&q=https://github.com/alok--kumar8765)**.
