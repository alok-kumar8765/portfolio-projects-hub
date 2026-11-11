# Colorful YouTube Video Downloader

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)
![GitHub Stars](https://img.shields.io/github/stars/alok--kumar8765/youtube-downloader?style=social)
![GitHub Forks](https://img.shields.io/github/forks/alok--kumar8765/youtube-downloader?style=social)

A sleek, responsive, and modern GUI application built with Python (`tkinter` and `yt-dlp`) that enables users to download YouTube videos or extract high-quality audio files seamlessly without GUI freezing.

---

## Table of Contents
- [Purpose & Utility](#purpose--utility)
- [Key Features](#key-features)
- [Requirements](#requirements)
- [Installation & Setup](#installation--setup)
- [File Structure](#file-structure)
- [System Architecture (DFD & ER Diagrams)](#system-architecture)
- [Pros and Cons](#pros-and-cons)
- [Limitations](#limitations)
- [Known Bugs & Vulnerabilities](#known-bugs--vulnerabilities)
- [Future Roadmap](#future-roadmap)
- [Contributing](#contributing)
- [Acknowledgements & Support](#acknowledgements--support)

---

## Purpose & Utility

The **Colorful YouTube Video Downloader** addresses the common issue of complex CLI-based video downloaders and unreliable web interfaces laden with ads. It provides a lightweight, clean, ad-free desktop app designed for fast video and audio archiving.

---

## Key Features

- **Asynchronous Downloading:** Multithreaded execution keeps the GUI 100% responsive during downloads.
- **Modern Dark UI:** Styled interface inspired by custom modern desktop app aesthetics.
- **Multiple Quality Options:** Grab best video quality (MP4) or extract standalone audio (MP3).
- **Real-time Download Metrics:** Live tracking of download percentage, transfer speed, and ETA.
- **Resilient Backend:** Powered by `yt-dlp` to ensure consistent performance despite YouTube API changes.

---

## Requirements

- **Python**: Version 3.8 or higher
- **FFmpeg**: Required for audio conversion (MP3) and merging high-res streams.
- **Python Packages**:
  - `yt-dlp`
  - `tk` (included standard with Windows/macOS Python installers)

---

## Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/alok--kumar8765/youtube-downloader.git
   cd youtube-downloader
   ```

2. **Set Up a Virtual Environment (Optional but Recommended)**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install yt-dlp
   ```

4. **Run the Application**
   ```bash
   python main.py
   ```

---

## File Structure

```text
youtube-downloader/
├── main.py              # Main application GUI and downloader logic
├── README.md            # Project documentation
├── requirements.txt     # Python dependencies
└── assets/              # Icons and application previews
```

---

## System Architecture

### Data Flow Diagram (DFD - Level 1)

```
 [User]
   │
   ├─── (1. Inputs URL & Options) ───► [ GUI Interface ]
   │                                         │
   │                                   (2. Pass Args)
   │                                         ▼
   │                                 [ Worker Thread ]
   │                                         │
   │                                   (3. Request Stream)
   │                                         ▼
   │  ◄── (5. Progress Updates) ────── [ yt-dlp Engine ] ◄──► [ YouTube Servers ]
   │                                         │
   └────── (6. File Saved) ◄────────── (4. Write File)
                                             ▼
                                     [ Local Storage ]
```

### Entity-Relationship Diagram (Conceptual Data Model)

```
 +------------------+            +------------------+
 |    USER_INPUT    | 1        * |  DOWNLOAD_JOB    |
 +------------------+            +------------------+
 | - url            |----------->| - job_id         |
 | - save_path      |            | - target_format  |
 | - format_choice  |            | - status         |
 +------------------+            | - progress_pct   |
                                 +------------------+
                                          | 1
                                          |
                                          | 1
                                 +------------------+
                                 |   OUTPUT_FILE    |
                                 +------------------+
                                 | - file_name      |
                                 | - file_path      |
                                 | - file_size      |
                                 +------------------+
```

---

## Pros and Cons

### Pros
- Fast download speeds using multi-threaded stream fetching.
- Completely free of advertisements and trackers.
- No GUI locking/freezing during high-bandwidth operations.

### Cons
- Requires `FFmpeg` installed system-wide for certain conversions.
- Lacks a built-in search bar (requires pasting URLs).

---

## Limitations

- Downloads are subject to network bandwidth capabilities.
- Age-restricted or region-locked videos may require additional cookie passing parameters.
- Download speeds may be throttled by YouTube's rate limiters during large file operations.

---

## Known Bugs & Vulnerabilities

- **FFmpeg Path Issue:** On systems where `ffmpeg` is not added to system environment variables, audio extraction (MP3) might throw an execution error.
- **Throttling:** Occasional slow downloads due to YouTube's strict signature rotation mechanisms. Updating `yt-dlp` (`pip install -U yt-dlp`) usually resolves this.

---

## Future Roadmap

- [ ] Playlist and batch URL download support.
- [ ] Video metadata preview (thumbnail, title, duration) before initiating download.
- [ ] Dark/Light theme toggle switch.
- [ ] Embedded search bar integration.

---

## Contributing

Contributions are welcome! Follow these steps to contribute:

1. Fork the Project repository.
2. Create your Feature Branch (`git checkout -b feature/NewFeature`).
3. Commit your Changes (`git commit -m 'Add NewFeature'`).
4. Push to the Branch (`git push origin feature/NewFeature`).
5. Open a Pull Request.

---

## Acknowledgements & Support

Thank you for checking out this project! 

If you found this tool useful, please consider giving it a ⭐ on GitHub!

Created with ❤️ by [alok--kumar8765](https://github.com/alok--kumar8765)