CAT-STRIKE: Multithreaded Desktop Overlay Engine
A lightweight Python-based prank tool that utilizes multithreading and real-time chroma-key processing to deploy interactive cat overlays based on user input.

Overview
CAT-STRIKE monitors system-wide mouse events to trigger synchronized video and audio overlays. It is designed to be harmless, resource-efficient, and easily deployable for testing or pranking purposes.

Core Features
Dual-Input Triggering:

Left Click: Deploys 'Huh Cat' at exact cursor coordinates.

Right Click: Deploys 'Maxwell Cat' (spinning) with synchronized audio.

Synchronized Frame Processing: Uses a background worker to keep video frames pre-processed in memory for zero-latency deployment.

Chroma-Key Rendering: Real-time green screen removal for transparent background overlays.

Automated Interaction: Integrated logic to trigger random system-style dialog boxes at 15-second intervals.

DPI Awareness: Native Windows API integration to ensure accurate coordinate mapping on high-resolution displays.

Installation
Ensure you have Python 3.8+ installed. Install the required dependencies via pip:

Bash
pip install opencv-python pynput numpy pygame screeninfo
Deployment
Clone the repository or download the source files.

Ensure the assets (huh_cat.mp4, maxwell.mp4, huh.wav, ding.wav) are in the root directory.

Execute the script:

Bash
python saka.py
To run the application as a background process (no console window), rename the main script to saka.pyw and execute it.

Termination
Terminal Mode: Focus the terminal and press CTRL + C.

Background Mode: Open Task Manager (CTRL + SHIFT + ESC) and end the Python process.

Disclaimer
This project is for educational and entertainment purposes. It does not modify system files or store user data.
