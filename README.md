# HARMONY – Human-Aware Waste Cleanup System

## Overview
HARMONY is an AI-powered waste cleanup system designed to detect waste and track its movement using computer vision. It uses object detection and Lucas–Kanade Optical Flow to analyze motion and identify waste movement toward a dustbin.

## Features
- Real-time object detection using YOLOv8.
- Motion tracking using Lucas–Kanade Optical Flow.
- Detection of people and waste objects.
- Movement analysis to help reduce false detections caused by occlusion.
- Audio feedback when the intended waste movement is detected.

## Technologies Used
- Python
- OpenCV
- YOLOv8
- Lucas–Kanade Optical Flow
- Pygame

## Project Structure
- `harmony_ai.py` – AI and object detection logic.
- `harmony_final.py` – Main project implementation.
- `test_cam.py` – Camera testing.
- `requirements.txt` – Python dependencies.

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/hrush08/Project-Harmony.git
   cd Project-Harmony
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv harmony_env
   harmony_env\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the project:
   ```bash
   python harmony_final.py
   ```

## Requirements
- Python
- Webcam
- Compatible Python packages listed in `requirements.txt`

## Author
HARMONY Project Team
