# USB Virus Removal Tool

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![OS: Windows](https://img.shields.io/badge/OS-Windows%2010%20%7C%2011-blue.svg)
![Language: Batch](https://img.shields.io/badge/Language-Batch%20%2F%20CMD-green.svg)
![Maintained: Yes](https://img.shields.io/badge/Maintained%3F-yes-brightgreen.svg)

An IT technician's utility script designed to safely remove USB shortcut malware, unhide hidden system files, delete `autorun.inf` files, and invoke an automated Microsoft Defender custom scan on the target drive.

**Project Owner:** GENERATIVE AI  
**GitHub Profile:** [alok--kumar8765](https://github.com/alok--kumar8765)

---

## Table of Contents
- [Purpose of This Project](#purpose-of-this-project)
- [Features](#features)
- [Requirements](#requirements)
- [Installation & Setup](#installation--setup)
- [How to Use](#how-to-use)
- [File Structure](#file-structure)
- [DFD Diagram](#dfd-diagram)
- [ER Diagram](#er-diagram)
- [Pros & Cons](#pros--cons)
- [Limitations](#limitations)
- [Bugs & Known Vulnerabilities](#bugs--known-vulnerabilities)
- [Future Updates](#future-updates)
- [Contributing](#contributing)
- [Star & Support](#star--support)
- [Thanks & Acknowledgments](#thanks--acknowledgments)

---

## Purpose of This Project
USB flash drives frequently get infected by shortcut malware across public, school, and office computers. This malware hides original files, replaces them with `.lnk` shortcuts, and drops malicious `autorun.inf` entry points. 

This project provides a reliable, lightweight script for IT technicians and everyday users to clean infected drives, regain file visibility, and perform an immediate Microsoft Defender scan without needing heavy third-party software installation.

---

## Features
- **Drive Validation:** Checks whether the specified drive letter actually exists before running actions.
- **Confirmation Guard:** Asks for confirmation before modifying or deleting any files.
- **Shortcut File Removal:** Deletes malicious `.lnk` shortcuts across the root directory.
- **Autorun Cleanup:** Strips attributes (`-h -r -s`) and removes `autorun.inf`.
- **File Restoration:** Unhides hidden, system, and read-only files and folders recursively using Windows `attrib`.
- **Automated Defender Scan:** Launches a custom Microsoft Defender scan on the cleaned USB drive via PowerShell.

---

## Requirements
- **Operating System:** Windows 10, Windows 11, or Windows Server.
- **Privileges:** Administrator access (required to run `attrib` and trigger Defender commands properly).
- **Security Software:** Built-in **Microsoft Defender** (Windows Defender) enabled.

---

## Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/alok--kumar8765/USB-Virus-Remover.git
   cd USB-Virus-Remover
   ```
2. Alternatively, copy the `.bat` script directly to your local computer.

---

## How to Use

1. Insert the infected USB flash drive into your computer.
2. Open Windows File Explorer and check the drive letter assigned to the USB drive (e.g., `E`, `F`, or `G`).
3. Right-click on `USB_Virus_Remover.bat` and select **Run as Administrator**.
4. Type your USB Drive Letter when prompted (e.g., `E`) and press `Enter`.
5. Type `Y` to confirm and start the cleanup process.
6. Wait for the file restoration and Microsoft Defender scan to complete.

---

## File Structure

```text
USB-Virus-Remover/
├── app.bat                      # Main execution script
├── README.md                    # Project documentation
└── LICENSE                      # MIT License file
```

---

## DFD Diagram

### Data Flow Diagram (Level 1)

```text
+-------------------+
|     User / IT     |
|    Technician     |
+---------+---------+
          |
          | 1. Input Drive Letter & Confirmation
          v
+---------+-------------------------------------------------+
|             USB Virus Removal Script                 |
|                                                           |
|  +--------------------+   +----------------------------+  |
|  | Drive Validation   |-->| Delete .lnk & autorun.inf  |  |
|  +--------------------+   +--------------+-------------+  |
|                                          |                |
|                                          v                |
|  +--------------------+   +----------------------------+  |
|  | Defender Scan      |<--| Restore Hidden Files       |  |
|  | Trigger            |   | (attrib -h -r -s)          |  |
|  +--------------------+   +----------------------------+  |
+---------+-------------------------------------------------+
          |
          | 2. File Updates & Defender Scan Trigger
          v
+---------+---------+
|     USB Drive     |
|   (Target Files)  |
+-------------------+
```

---

## ER Diagram

Since batch script operations are file-system based rather than relational database based, the Entity-Relationship (ER) model reflects the interaction between logical entities:

```text
+-------------------+             1:N             +-------------------+
|     USER / IT     |---------------------------->|     USB DRIVE     |
|    TECHNICIAN     |  Executes Cleanup Script    |  (Target Storage) |
+-------------------+                             +---------+---------+
                                                            |
                                                            | 1:N Contains
                                                            v
                                                  +-------------------+
                                                  |    FILE SYSTEM    |
                                                  | - Shortcuts (.lnk)|
                                                  | - autorun.inf     |
                                                  | - Hidden Files    |
                                                  +-------------------+
```

---

## Pros & Cons

### Pros
- **Fast & Lightweight:** Runs natively in Windows CMD without installing third-party tools.
- **Safe Execution:** Confirms drive letter validity and prompts user before taking action.
- **Restores Missing Data:** Quickly fixes the common "missing folder" panic caused by shortcut viruses.

### Cons
- **Windows Only:** Cannot be executed on macOS or Linux environments.
- **Requires Admin Rights:** Requires elevated privileges to modify system attributes and run Defender commands.

---

## Limitations
- **Not a Full Antivirus:** This script removes symptoms (shortcuts, hidden flags, autorun files) and triggers Defender; it does not replace real-time anti-malware protection.
- **Batch Scope:** Cannot clean infected file payloads embedded inside legitimate `.exe` or executable files.

---

## Bugs & Known Vulnerabilities
- **Drive Letter Misconfiguration:** Entering a local OS drive letter (e.g., `C`) could strip file attributes on system files if confirmation is bypassed. (Mitigated by input validation and confirmation steps).
- **Defender Dependency:** If Microsoft Defender is disabled or replaced by third-party antivirus software, the PowerShell command `Start-MpScan` may return an error.

---

## Future Updates
- [ ] Add auto-detection of removable drives to eliminate manual drive letter entry.
- [ ] Add log file output (`cleanup_log.txt`) to record cleaned files and execution timestamps.
- [ ] Add support for third-party antivirus CLI integration (e.g., Avast, Bitdefender).
- [ ] GUI-based wrapper using PowerShell / WPF.

---

## Contributing
Contributions are welcome! If you'd like to improve the script or add new features:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## Star & Support
If this script saved your files or helped your IT workflow, please consider giving this repository a ⭐ on GitHub!

---

## Thanks & Acknowledgments
- Thanks to the IT technician community for documenting common USB malware behavior.
- Developed by **GENERATIVE AI** for **GENERATIVE AI**.
- Maintained by [@alok--kumar8765](https://github.com/alok--kumar8765).