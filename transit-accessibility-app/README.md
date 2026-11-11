# 🏙️ Urban Accessibility & "15-Minute City" Analyzer

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-FF4B4B.svg)](https://streamlit.io/)
[![Folium](https://img.shields.io/badge/Folium-0.15%2B-77B829.svg)](https://python-visualization.github.io/folium/)
[![OSMnx](https://img.shields.io/badge/OSMnx-1.8%2B-000000.svg)](https://osmnx.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An interactive, data-driven geospatial web application built with **Python**, **Streamlit**, **Folium**, and **OSMnx**. This tool evaluates urban walkability and infrastructure accessibility by generating metric spatial buffers around user-defined center points and fetching real-time OpenStreetMap (OSM) points of interest.

---

## 📜 Table of Contents

- [Overview & Purpose](#-overview--purpose)
- [Key Features](#-key-features)
- [System Architecture & Diagrams](#-system-architecture--diagrams)
  - [Data Flow Diagram (DFD)](#data-flow-diagram-dfd)
  - [Entity-Relationship (ER) Diagram](#entity-relationship-er-diagram)
- [File Structure](#-file-structure)
- [Requirements](#-requirements)
- [Installation & Setup](#-installation--setup)
- [How to Use](#-how-to-use)
- [Pros & Cons](#-pros--cons)
- [Limitations](#-limitations)
- [Known Bugs & Vulnerabilities](#-known-bugs--vulnerabilities)
- [Future Roadmap](#-future-roadmap)
- [Contributing](#-contributing)
- [License & Acknowledgments](#-license--acknowledgments)

---

## 🎯 Overview & Purpose

The concept of the **"15-Minute City"** emphasizes that all essential human needs (healthcare, education, food, recreation) should be accessible within a short walk or bike ride from any residential point. 

The **Urban Accessibility Analyzer** turns abstract geospatial concepts into actionable visual intelligence. It allows urban planners, data analysts, and local residents to compute real-time spatial buffers, evaluate amenity density, and inspect urban infrastructure anywhere in the world using vector data straight from OpenStreetMap.

---

## ✨ Key Features

- 🌍 **Global Geocoding:** Search any neighborhood, address, or city globally via OpenStreetMap's Nominatim engine.
- 📐 **Accurate Metric Buffering:** Uses projected UTM coordinate reference systems (CRS) via GeoPandas and Shapely for millimeter-accurate geodesic buffers.
- ⚡ **Dynamic OSM Querying:** On-demand fetching of points of interest (hospitals, schools, cafes, parks, etc.) within the exact spatial radius.
- 🗺️ **Interactive Folium Maps:** Embedded custom interactive web map with dynamic markers, tooltips, popups, and visual bounds.
- 🚀 **Streamlit Caching:** Optimized query handling via `@st.cache_data` to minimize network overhead and ensure instantaneous UI response.

---

## 📐 System Architecture & Diagrams

### Data Flow Diagram (DFD)

```
 [ User Input ] (City, Amenity, Walking Radius)
       │
       ▼
 [ Streamlit Sidebar UI ]
       │
       ▼
 [ Nominatim API / OSMnx Geocoder ] ──► Converts text address to (Lat, Lon)
       │
       ▼
 [ GeoPandas & Shapely Engine ] ─────► Projects WGS84 to local UTM zone & creates spatial Buffer
       │
       ▼
 [ Overpass API / OSM Features ] ────► Fetches matching Amenity Polygons/Points within Buffer
       │
       ▼
 [ Folium Rendering Engine ] ───────► Generates Leaflet HTML Map with Markers & Polygons
       │
       ▼
 [ Interactive Screen Output ]
```

### Entity-Relationship (ER) Diagram

```
+--------------------------------+       1 : N       +--------------------------------+
|       TARGET LOCATION          |-------------------|           AMENITY              |
+--------------------------------+                   +--------------------------------+
| PK  location_id   : UUID       |                   | PK  amenity_id    : BigInt     |
|     address_name  : String     |                   | FK  location_id   : UUID       |
|     latitude      : Float      |                   |     name          : String     |
|     longitude     : Float      |                   |     category      : String     |
|     buffer_radius : Integer    |                   |     latitude      : Float      |
|     crs_projection: String     |                   |     longitude     : Float      |
+--------------------------------+                   +--------------------------------+
```

---

## 📁 File Structure

```text
transit-accessibility-app/
│
├── .gitignore              # Ignored files (venv, cache, temporary files)
├── app.py                  # Main Streamlit web application & spatial pipeline
├── README.md               # Project documentation
└── requirements.txt        # Python package dependencies
```

---

## 📦 Requirements

- **Python:** `3.9` or higher
- **Core Dependencies:**
  - `streamlit >= 1.32.0`
  - `folium >= 0.15.0`
  - `streamlit-folium >= 0.17.0`
  - `osmnx >= 1.8.0`
  - `geopandas >= 0.14.0`
  - `shapely >= 2.0.0`
  - `pandas >= 2.0.0`

---

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/alok--kumar8765/transit-accessibility-app.git
   cd transit-accessibility-app
   ```

2. **Create and activate a Virtual Environment:**
   - **Linux/macOS:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - **Windows:**
     ```cmd
     py -m venv venv
     venv\Scripts\activate
     ```

3. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

5. Access the app locally in your browser at `http://localhost:8501`.

---

## 🕹️ How to Use

1. Open the left **Configuration Panel** in the Streamlit web interface.
2. Enter a **Target Location** (e.g., `Prenzlauer Berg, Berlin, Germany` or `Manhattan, New York`).
3. Select an **Amenity Category** from the dropdown menu (e.g., `hospital`, `school`, `cafe`, `pharmacy`).
4. Adjust the **Walking Radius** slider (from 200m to 1500m).
5. Inspect the interactive map, count metrics, and expand the raw data tab below the visualization.

---

## ⚖️ Pros & Cons

### Pros
- 🟢 **Zero API Keys Required:** Uses open infrastructure (OpenStreetMap & Overpass API).
- 🟢 **High Mathematical Rigor:** Converts geographic coordinates to local projected UTM zones for precise distance buffers.
- 🟢 **Lightweight & Fast:** High-performance caching prevents redundant network calls.

### Cons
- 🔴 **Network Dependent:** Requires an active internet connection to contact OSM services.
- 🔴 **API Rate Limits:** High-frequency requests can occasionally trigger Overpass API throttling.

---

## ⚠️ Limitations

- **Euclidean vs. Network Distance:** The walking buffer uses a radial geodesic distance (as the crow flies) rather than strict street-network routing paths (isochrones).
- **OSM Data Completeness:** Accuracy depends on community contributions to OpenStreetMap in specific geographic regions.

---

## 🔒 Known Bugs & Vulnerabilities

- **OSM Rate Limits:** Submitting rapid location changes within seconds may cause a temporary `504 Gateway Timeout` from the Overpass servers.
- **Geocoding Ambiguity:** Vague search inputs (e.g., "Springfield") may default to an unintended location without an explicit country/state qualifier.

---

## 🛣️ Future Roadmap

- [ ] **True Isochrone Calculation:** Integrate street-network walking paths via NetworkX / OSRM.
- [ ] **Multi-Amenity Layers:** Allow users to overlay multiple amenity types (e.g., parks + transit simultaneously).
- [ ] **Export Options:** Enable GeoJSON and PDF report downloads for urban planners.
- [ ] **Demographic Overlay:** Layer census or population density data into the spatial buffer.

---

## 🤝 Contributing

Contributions are welcome! Follow these steps to contribute:

1. Fork the project repository.
2. Create your Feature Branch (`git checkout -b feature/AwesomeFeature`).
3. Commit your changes (`git commit -m 'Add awesome feature'`).
4. Push to the Branch (`git push origin feature/AwesomeFeature`).
5. Open a Pull Request.

---

## 🌟 Acknowledgments & Support

If you found this project helpful, please give it a **⭐ Star** on [GitHub](https://github.com/alok--kumar8765)!

Special thanks to the open-source developers behind **Streamlit**, **OSMnx**, **GeoPandas**, and the **OpenStreetMap** community.

---
**Maintained by:** [@alok--kumar8765](https://github.com/alok--kumar8765)