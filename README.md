# Fall Detection System with Raspberry Pi

A smart fall detection system using Raspberry Pi, computer vision, and cloud computing to monitor human falls in real time. The system captures video from a camera, analyzes body posture using MediaPipe Pose, and sends emergency alerts through Telegram when a fall is detected.

## Overview

This project was developed for the course **NT131 – Wireless Embedded Systems** at the University of Information Technology (UIT - VNUHCM).

The system is designed to support elderly people, patients, or individuals living alone by automatically detecting fall incidents and triggering alerts immediately.

## Features

- Real-time fall detection using camera input
- Human pose estimation with MediaPipe Pose
- Raspberry Pi integration
- Cloud-based image processing server
- Telegram alert notification
- Buzzer alarm activation
- Fall event logging on Google Cloud Storage
- Web dashboard for monitoring and statistics
- Raspberry Pi system resource monitoring

---

## System Architecture

```text
Camera → Raspberry Pi → Cloud Server (FastAPI)
                              ↓
                    MediaPipe Pose Detection
                              ↓
               Fall Detection Algorithm
                              ↓
         Telegram Alert + Buzzer + Web Dashboard
```
## Technologies Used

### Hardware
- Raspberry Pi 3 Model B+
- Logitech C270 Camera
- Buzzer Module

### Software & Services
- Python
- FastAPI
- MediaPipe Pose
- Google Cloud Platform (GCP)
- Google Compute Engine
- Google Cloud Storage
- Telegram Bot API

---

## Hardware Setup

### Components

| Component | Description |
|---|---|
| Raspberry Pi 3 Model B+ | Main embedded device |
| Logitech C270 | Camera for video capture |
| Buzzer Module | Audio alert system |

### Buzzer Wiring

| Buzzer Pin | Raspberry Pi Pin |
|---|---|
| VCC | Pin 1 (3.3V) |
| I/O | Pin 11 (GPIO17) |
| GND | Pin 9 (GND) |

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/hoangle795/NT131.git
cd NT131
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Raspberry Pi

Install Raspberry Pi OS using Raspberry Pi Imager.

Enable:
- Camera
- SSH/VNC
- Internet connection

### 4. Configure Telegram Bot

Create a Telegram bot using BotFather and obtain:
- BOT_TOKEN
- CHAT_ID

Update configuration file:

```python
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
```

### 5. Configure Google Cloud

Create:
- Compute Engine VM
- Cloud Storage Bucket

Upload service account credentials:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="service-account.json"
```

---

## Running the System

### Start Server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Run Raspberry Pi Client

```bash
python raspberry_pi_client.py
```

---

## Fall Detection Workflow

1. Camera captures real-time frames
2. Raspberry Pi sends images to the server
3. Server processes images using MediaPipe Pose
4. Body landmarks are analyzed
5. Fall detection algorithm determines fall state
6. If a fall is detected:
   - Telegram alert is sent
   - Buzzer is activated
   - Event image and logs are stored
   - Dashboard is updated

---

## Detection Algorithm

The system analyzes:
- Shoulder-to-hip height ratio
- Hip-to-foot geometry
- Body orientation
- Human pose landmarks

The algorithm classifies:
- Standing
- Bending
- Falling

---

## Web Dashboard

The management website includes:
- User authentication
- Live camera monitoring
- Fall image display
- Raspberry Pi resource monitoring
- Fall statistics visualization
- Alarm reset functionality

---

## Project Structure

```text
project/
│
├── raspberry_pi/
│   ├── client.py
│   ├── buzzer.py
│   └── telegram_alert.py
│
├── server/
│   ├── main.py
│   ├── detect_fall.py
│   ├── pose_processing.py
│   └── cloud_storage.py
│
├── web_dashboard/
│
├── requirements.txt
└── README.md
```

---

## Future Improvements

- Mobile application integration
- Multi-device management
- Improved AI detection accuracy
- Docker & Kubernetes deployment
- Accelerometer sensor integration
- Automatic lighting support

---

## Team Members

| Name | Student ID |
|---|---|
| Nguyễn Hoàng Lộc | 23520858 |
| Huỳnh Minh Khoa | 23520738 |
| Lê Xuân Hoàng | 23520524 |

---

## Course Information

- Course: NT131 – Wireless Embedded Systems
- Faculty: Computer Networks and Communications
- University: University of Information Technology – VNUHCM

---

## References

- MediaPipe Pose
- FastAPI Documentation
- Google Cloud Documentation
- Telegram Bot API

---

## License

This project is developed for educational and research purposes.