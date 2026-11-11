# 🎹 Python Synthesizer & Yamaha-Style Workstation

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/pygame-2.6.1-green.svg)](https://www.pygame.org/)
[![NumPy](https://img.shields.io/badge/numpy-supported-orange.svg)](https://numpy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub Owner](https://img.shields.io/badge/GitHub-alok--kumar8765-lightgrey?logo=github)](https://github.com/alok--kumar8765)

An interactive, lightweight graphical piano synthesizer and audio workstation built completely in Python using **Tkinter** for the UI, **Pygame** for real-time audio mixing, and **NumPy** for mathematical sine-wave synthesis and envelope shaping.

---

## 📖 Table of Contents
1. [Purpose of This Project](#-purpose-of-this-project)
2. [Use Cases](#-use-cases)
3. [Features](#-features)
4. [File Structure](#-file-structure)
5. [Requirements](#-requirements)
6. [Installation & Setup](#-installation--setup)
7. [System Architecture: DFD Diagram](#-system-architecture-dfd-diagram)
8. [Data Relationships: ER Diagram](#-data-relationships-er-diagram)
9. [Pros and Cons](#-pros-and-con)
10. [Limitations](#-limitations)
11. [Bugs & Vulnerabilities](#-bugs-and-vulnerabilities)
12. [Future Updates](#-future-updates)
13. [Contributing](#-contributing)
14. [Author & Acknowledgments](#-author--acknowledgments)

---

## 🎯 Purpose of This Project
The primary purpose of this project is to bridge the gap between low-level computer science mathematics (digital signal processing) and high-level graphical user interface development in Python. It demonstrates how frequency formulas ($f = f_0 \cdot 2^{n/12}$), exponential decay envelopes, and real-time event handling can be combined to build a functional musical instrument without relying on heavy external digital audio workstations (DAWs).

## 💡 Use Cases
* **Educational Tool:** Teaching students how sound waves, frequencies, and overtones work mathematically using NumPy.
* **Prototyping:** A lightweight reference design for building custom Python-based GUI soundboards and keyboard utilities.
* **Casual Entertainment:** Playing melodies directly from your computer keyboard or via automated playback demos like Beethoven's *Ode to Joy*.

---

## ✨ Features
* **Yamaha-Style Keyboard Layout:** Full visual representation of white and black keys spanning two octaves.
* **Dual Input Support:** Play notes seamlessly using either your computer keyboard or mouse clicks.
* **Interactive Audio Mixer Panel:**
  * **Master Volume Control:** Adjust output gain in real time.
  * **Sustain / Decay Slider:** Modify how fast notes fade out.
  * **Overtone Richness Slider:** Blend fundamental sine waves with harmonic frequencies for richer tone timbre.
* **Visual Key Feedback:** Keys light up instantly upon activation.
* **Automated Demo Mode:** Built-in player executing *Ode to Joy*.

---

## 📂 File Structure
```text
Piano/
│
├── Advanced_UI_Piano.py    # Main application file containing GUI, Synth Engine, and Mixer logic
└── README.md               # Project documentation
```

---

## ⚙️ Requirements
* **Python 3.8+**
* **NumPy** (for mathematical audio array generation)
* **Pygame** (for low-latency audio mixing and hardware device handling)

---

## 🚀 Installation & Setup

1. **Clone or Download the Repository:**
   ```bash
   git clone https://github.com/alok--kumar8765/python-piano-synthesizer.git
   cd python-piano-synthesizer
   ```

2. **Create and Activate a Virtual Environment (Recommended):**
   ```bash
   python -m venv env
   # On Windows:
   env\Scripts\activate
   # On macOS/Linux:
   source env/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install numpy pygame
   ```

4. **Run the Application:**
   ```bash
   python Advanced_UI_Piano.py
   ```

---

## 📊 System Architecture: DFD Diagram
Data Flow Diagram (Level 1) representing how user inputs travel through the system:

```text
[ User / Mouse / Keyboard ]
           │
           ▼  (Key Events / Slider Values)
   ┌───────────────┐
   │ Tkinter UI    │ ──(Update Mixer/Canvas)──> [ Graphical Display ]
   └───────────────┘
           │
           ▼  (Frequency & Mixer States)
   ┌───────────────┐
   │ NumPy Engine  │ ──(Generate Sine Wave + Envelope Array)──> [ Stereo Array ]
   └───────────────┘
           │
           ▼
   ┌───────────────┐
   │ Pygame Mixer  │ ──(Sound Buffer Output)──> [ Hardware Speakers ]
   └───────────────┘
```

---

## 🗂️ Data Relationships: ER Diagram
Entity-Relationship representation of the core application config structures:

```text
+-------------------+          +---------------------+          +-------------------+
|    KEY_CONFIGS    | 1 ---- n |   TkinterCanvas     | 1 ---- 1 |    AudioMixer     |
+-------------------+          +---------------------+          +-------------------+
| - char (PK)       |          | - canvas_id         |          | - volume_var      |
| - note_name       |          | - rect_reference    |          | - decay_var       |
| - semitone_offset |          | - highlight_color   |          | - harmonic_var    |
| - key_type        |          +---------------------+          +-------------------+
+-------------------+
```

---

## ⚖️ Pros and Cons

### **Pros:**
* Zero external audio sample files required (everything is algorithmically generated on-the-fly).
* Highly responsive event binding with minimal input lag.
* Clean separation of concerns between UI rendering, sound synthesis, and event management within a single script.

### **Cons:**
* Monophonic/Polyphonic limits depend on Pygame channel allocation limits.
* Built-in envelope uses a simple exponential formula rather than a multi-stage ADSR envelope.

---

## ⚠️ Limitations
* Restricted to the pre-configured key mapping range (~two octaves).
* Window dimensions and layout scales are static and non-responsive to window resizing.

---

## 🐛 Bugs and Vulnerabilities
* **Audio Clipping:** Extreme settings on the overtone richness slider combined with maximum master volume can occasionally cause slight digital clipping if audio output exceeds 16-bit PCM integer boundaries.
* **Key Release Stacking:** Rapid multi-key typing can occasionally leave keys highlighted if key release events fire out of sync with rapid window focus loss.

---

## 🔮 Future Updates
* [ ] **ADSR Envelope Control:** Add Attack, Decay, Sustain, and Release knobs to the UI mixer.
* [ ] **MIDI Controller Support:** Integrate `mido` or `pygame.midi` to plug in external USB keyboards.
* [ ] **Recording Feature:** Save live performances directly to `.wav` files.
* [ ] **Multi-Octave Toggle:** Add shift buttons to transpose the keyboard up and down octaves.

---

## ⭐ Support & Star this Repository
If you found this project helpful, educational, or fun, please consider giving it a ⭐ on GitHub! It helps motivate future updates and open-source contributions.

GitHub Profile: [alok--kumar8765](https://github.com/alok--kumar8765)

---

## 🤝 Contributing
Contributions, bug reports, and feature requests are welcome! 
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git origin push feature/AmazingFeature`)
5. Open a Pull Request

---

## 🙏 Thanks
A special thanks to the open-source community behind Python, NumPy, and Pygame for making low-level audio programming accessible and enjoyable.