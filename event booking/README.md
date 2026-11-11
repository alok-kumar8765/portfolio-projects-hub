# 🎫 Event & Ticket Booking System

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![GUI Framework](https://img.shields.io/badge/GUI-Tkinter-orange.svg)
![Database](https://img.shields.io/badge/Database-SQLite%2FMySQL-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-brightgreen.svg)

A modern desktop application built with Python and Tkinter for seamlessly managing events, online ticket bookings, customer databases, and revenue analytics dashboard visualizations. Designed with multi-theme support and a clean interface inspired by Eventbrite.

---

## 📐 Table of Contents
- [📌 Purpose & Overview](#-purpose--overview)
- [✨ Features](#-features)
- [📦 Requirements](#-requirements)
- [🚀 Installation & Setup](#-installation--setup)
- [📂 File Structure](#-file-structure)
- [📊 DFD Diagram](#-dfd-diagram)
- [🗄️ ER Diagram](#-er-diagram)
- [⚖️ Pros & Cons](#%EF%B8%8F-pros--cons)
- [⚠️ Limitations](#%EF%B8%8F-limitations)
- [🔒 Known Bugs & Vulnerabilities](#-known-bugs--vulnerabilities)
- [🔮 Future Updates](#-future-updates)
- [🤝 Contributing](#-contributing)
- [⭐ Thanks & Support](#-thanks--support)

---

## 📌 Purpose & Overview

The **Event & Ticket Booking System** is designed to streamline event organization and ticketing workflows for event planners and small businesses. It replaces complex web infrastructure with a self-contained desktop system capable of managing attendees, monitoring live revenue analytics, updating booking statuses, and switching themes dynamically.

---

## ✨ Features

- **📊 Dashboard & Live Analytics:** Visual bar charts and status distribution for quick metrics overview.
- **📅 Event Management:** Create, update, and manage event schedules, locations, and seating caps.
- **🎫 Ticket Booking Engine:** Integrated customer-to-event ticket issuance workflow.
- **📋 Booking Status Tracking:** Change booking status (Pending, Confirmed, Cancelled) in real time.
- **👥 Customer Directory:** Comprehensive database management for registered attendees.
- **🎨 Multi-Theme GUI Engine:** Instantly switch between *Modern Dark*, *Light Clean*, and *Cyberpunk* themes.
- **🔐 User Authentication:** Embedded login and secure session logout controls.

---

## 📦 Requirements

- **Python:** Version `3.8` or higher
- **Standard Libraries:** `tkinter`, `sqlite3`, `datetime`
- **Optional (for MySQL setup):** `mysql-connector-python`

---

## 🚀 Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/alok--kumar8765/event-booking-system.git
   cd event-booking-system
   ```

2. **Create a Virtual Environment (Optional but Recommended)**
   ```bash
   python -m venv env
   # On Windows
   env\Scripts\activate
   # On macOS/Linux
   source env/bin/activate
   ```

3. **Install Dependencies**
   *(SQLite comes pre-installed with standard Python distributions)*
   ```bash
   pip install mysql-connector-python
   ```

4. **Run the Application**
   ```bash
   python app.py
   ```
   *Default Credentials:*
   - **Username:** `admin`
   - **Password:** `admin`

---

## 📂 File Structure

```text
event-booking-system/
├── app.py                 # Main application script (GUI + Logic + DB Initialization)
├── event_db.sqlite        # Auto-generated local SQLite database engine
├── README.md              # Project documentation
└── assets/                # Application banners and icons (optional)
```

---

## 📊 DFD Diagram

```text
+------------------+          1.0 Authenticate          +---------------------+
|                  | ---------------------------------> |                     |
|      Admin       |                                    |  Authentication     |
|     User         | <--------------------------------- |      Module         |
|                  |          Session Granted           +---------------------+
+------------------+                                               |
         |                                                         v
         | 2.0 Select Action (Events/Bookings/Reports)     +---------------------+
         +-----------------------------------------------> |   Control Panel     |
                                                           |   & Interface       |
                                                           +---------------------+
                                                                |          |
                      +-----------------------------------------+          +-----------------------------------------+
                      | 3.0 Process Bookings                                                                         | 4.0 Query Analytics
                      v                                                                                              v
           +---------------------+                                                                        +---------------------+
           | Ticket Booking      | <====================================================================> | SQLite / MySQL      |
           | Module              |                     Store & Fetch Details                              | Database            |
           +---------------------+                                                                        +---------------------+
```

---

## 🗄️ ER Diagram

```text
 +-------------------+         1         N         +-------------------+
 |      EVENTS       | --------------------------< |     BOOKINGS      |
 +-------------------+                             +-------------------+
 | event_id (PK)     |                             | booking_id (PK)   |
 | event_name        |                             | event_id (FK)     |
 | event_date        |                             | customer_name     |
 | location          |                             | quantity          |
 | price             |                             | booking_date      |
 | seats             |                             | status            |
 +-------------------+                             +-------------------+
                                                            |
                                                            | N
                                                            |
                                                            | 1
                                                   +-------------------+
                                                   |     CUSTOMERS     |
                                                   +-------------------+
                                                   | customer_id (PK)  |
                                                   | name              |
                                                   | email             |
                                                   | phone             |
                                                   +-------------------+
```

---

## ⚖️ Pros & Cons

| Pros 🟢 | Cons 🔴 |
| :--- | :--- |
| **Zero External Server Setup:** Runs locally out-of-the-box using SQLite. | **Single-Device Access:** Desktop GUI lacks native web client access. |
| **Lightweight & Fast:** Starts instantly with negligible resource utilization. | **Basic Charting Engine:** Canvas-rendered charts instead of heavy web charts. |
| **Highly Customizable Themes:** Built-in dynamic theme switcher engine. | **No Multi-Role RBAC:** Currently limited to single admin account context. |

---

## ⚠️ Limitations

- **Concurrency:** SQLite database locks during concurrent write operations if accessed simultaneously by multiple network instances.
- **Payment Processing:** No native integration with third-party payment gateways (Stripe/PayPal).
- **Notification Services:** Email ticket delivery/SMS updates are currently non-functional without external gateway API integration.

---

## 🔒 Known Bugs & Vulnerabilities

1. **Plaintext Local Credentials:** Hardcoded fallback authentication credentials in script logic (`admin` / `admin`).
2. **Input Validation:** Extended character length inputs in table forms may overflow default display frame constraints.

---

## 🔮 Future Updates

- [ ] Add PDF Ticket Generation & QR Code Verification system.
- [ ] Implement password hashing (`bcrypt`) and user role management.
- [ ] Integrate Matplotlib for interactive chart zooming and export support.
- [ ] Add REST API bridge for web/mobile client synchronisation.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!  
Feel free to check out the [issues page](https://github.com/alok--kumar8765/event-booking-system/issues).

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/NewFeature`)
3. Commit your Changes (`git commit -m 'Add NewFeature'`)
4. Push to the Branch (`git checkout origin feature/NewFeature`)
5. Open a Pull Request

---

## ⭐ Thanks & Support

If this project helped you learn or build something cool, please give it a **⭐ Star** on GitHub!

Developed by **[alok--kumar8765](https://github.com/alok--kumar8765)**  
Creator Credit: **Generative AI | Copyrights 2026**