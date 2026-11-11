# Smart Attendance System (Pro Edition)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0%2B-green.svg)](https://flask.palletsprojects.com/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-red.svg)](https://opencv.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey.svg)](https://www.sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern, lightweight web-based attendance tracking and management system built using **Flask**, **OpenCV**, and **SQLite**. It shifts camera processing streams to the client browser via WebRTC/Canvas APIs, prevents single-point database locking, offers dynamic multi-theme UI layouts, and supports advanced analytical filters, parent information mapping, and custom date-range reporting.

---

## Table of Contents
1. [Features](#features)
2. [Architecture & System Design](#architecture--system-design)
3. [Folder Structure](#folder-structure)
4. [Setup & Installation](#setup--installation)
5. [Usage Guide](#usage-guide)
6. [Use Cases](#use-cases)
7. [Pros & Cons](#pros--cons)
8. [Limitations & Known Bugs](#limitations--known-bugs)
9. [Security Vulnerabilities](#security-vulnerabilities)
10. [Future Enhancements](#future-enhancements)
11. [Contributing](#contributing)
12. [Author](#author)

---

## Features
* **Client-Side Camera Capture:** Secure browser-based webcam stream handling via HTML5 MediaDevices API.
* **Student Lifecycle Management:** Register students with Roll Numbers, Full Names, and Parent Details (Father's & Mother's names).
* **Advanced Analytics & Filtering:** View aggregate attendance, filter by **Monthly**, **Yearly**, or **Low Attendance (<75%)**, and search instantly across names or parent identities.
* **Custom Reporting Engine:** Generate targeted logs for individual students or the entire institution over custom date ranges.
* **Multi-Theme Interface:** Includes toggleable UI themes (Dark Modern, Cyberpunk Neon, and Clean Light).
* **Automatic Database Migrations:** Safe schema upgrades via SQLite pragma checks.

---

## Architecture & System Design

### High-Level Architecture Diagram
```text
┌────────────────────────┐         REST API (JSON / Base64)        ┌────────────────────────┐
│                        │ ──────────────────────────────────────> │                        │
│   Frontend Client      │                                         │   Flask Backend Server │
│   (HTML5 / JS / WebRTC)│ <────────────────────────────────────── │   (app.py / OpenCV)    │
└────────────────────────┘          Success / Data Payloads        └───────────┬────────────┘
                                                                               │
                                                                               ▼
                                                                   ┌────────────────────────┐
                                                                   │     SQLite Database    │
                                                                   │     (attendance.db)    │
                                                                   └────────────────────────┘

```

### Data Flow Diagram (DFD - Level 1)

1. **Capture:** Client browser initializes media stream $\rightarrow$ User selects student $\rightarrow$ Captures canvas snapshot.
2. **Transmit:** Frame encoded as Base64 payload $\rightarrow$ Sent via HTTP POST to `/api/mark`.
3. **Process:** Backend decodes image $\rightarrow$ Runs OpenCV Haar cascade face validation check.
4. **Persist:** Checks duplicate attendance for current date $\rightarrow$ Commits records into SQLite relational schema.

### Entity-Relationship (ER) Diagram Schema

* **STUDENTS (`1`)** ──< **ATTENDANCE (`N`)**
* `students` (id [PK], student_code [UK], name, father_name, mother_name)
* `attendance` (id [PK], student_id [FK], timestamp, status)



---

## Folder Structure

```text
smart-attendance/
│
├── app.py                  # Flask backend server & SQLite ORM logic
├── attendance.db           # SQLite database (auto-generated)
├── templates/
│   └── index.html          # Modern frontend dashboard UI (HTML/CSS/JS)
└── README.md               # Project documentation

```

---

## Setup & Installation

### Prerequisites

* Python 3.8 or higher installed on your system.
* A working webcam device.

### Step-by-Step Installation

1. **Clone the repository:**
```bash
git clone [https://github.com/alok-kumar8765/smart-attendance.git](https://github.com/alok-kumar8765/smart-attendance.git)
cd smart-attendance

```


2. **Install required dependencies:**
```bash
pip install flask opencv-python numpy

```


3. **Run the application:**
```bash
python app.py

```


4. **Access in browser:**
Open your browser and navigate to: `http://localhost:5000`

---

## Usage

1. **Register Students:** Go to the **Add Student** tab, input Roll Number, Name, and Parent details, then save.
2. **Mark Attendance:** Go to the **Mark Attendance** tab, allow webcam permissions, select the student profile, and click **Capture & Mark Attendance**.
3. **Analyze Records:** Switch to **Analytics & Filters** to search data or track low attendance (<75%).
4. **Export Reports:** Choose a student profile or leave blank, specify a date range in the **Reports** tab, and generate logs.

---

## Pros & Cons

### Pros

* Lightweight, runs entirely locally without heavy cloud instances or paid database servers.
* Browser-based client camera abstraction solves remote server video streaming bottlenecks.
* Highly responsive design with multiple customizable user themes.

### Cons

* Relies on manual dropdown selection instead of automated computer vision vector face-matching (in current baseline setup).
* SQLite concurrency limits high-volume enterprise production throughput.

---

## Limitations & Known Bugs

* **Limitations:** SQLite does not support highly concurrent multi-threaded write scaling out-of-the-box.
* **Known Bugs:** Direct browser camera initialization will fail if served over insecure HTTP when accessed from non-localhost external network IPs (requires HTTPS or local loopback).

---

## Security Vulnerabilities

* **Spoofing Risk:** Static image capture via webcam can be spoofed by presenting a photograph or phone screen to the camera (mitigated by adding liveness detection modules in future scopes).
* **Input Sanitization:** Basic parameters protected via parameterized SQL queries against SQL injection, but payload body size constraints should be enforced for production proxy safety.

---

## Future Enhancements

* Integration of `InsightFace` / `DeepFace` vector embeddings for automatic face identification.
* Active/Passive liveness detection anti-spoofing checks.
* Automated SMS/WhatsApp notifications via Twilio API for absentee tracking.
* Export data features directly into downloadable CSV and PDF files.

---

## Contributing

Contributions are welcome! Please feel free to fork this repository, submit pull requests, or open issues for feature suggestions.

1. Fork the Project (`https://github.com/alok-kumar8765/smart-attendance`)
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git origin push feature/AmazingFeature`)
5. Open a Pull Request

---

## Author

* **GitHub:** [alok-kumar8765](https://github.com/alok-kumar8765)
