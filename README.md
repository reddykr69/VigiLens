# VigiLens 🎥

### A Real-Time Video Surveillance System for Detection of Abandoned Objects

![Python](https://img.shields.io/badge/Python-3.13-blue)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-green)
![PyQt5](https://img.shields.io/badge/GUI-PyQt5-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📌 About the Project

VigiLens is an AI-powered standalone Windows desktop application that automatically monitors live camera feeds and recorded CCTV footage to detect abandoned or unattended objects in real time. The system uses deep learning based object detection combined with a proprietary ownership association module to intelligently determine whether an object has been genuinely abandoned by its owner, reducing false alarms and improving security response time.

---

## 🚨 Problem Statement

Traditional CCTV surveillance systems rely entirely on manual monitoring by security personnel which leads to human fatigue, missed incidents, and delayed response times. There is no automated mechanism to identify whether an object has been genuinely abandoned or is simply temporarily stationary. Commercial AI surveillance solutions that address this are expensive and require complex server infrastructure making them inaccessible for small institutions and organizations.

---

## ✅ Proposed Solution

VigiLens addresses these gaps by providing an affordable, intelligent, and lightweight standalone desktop application that automatically detects abandoned objects without requiring constant human attention or expensive infrastructure.

---

## 🎯 Features

- Real-time object detection using YOLOv8s deep learning model
- Ownership association module linking each object to its nearest person
- Abandoned object detection with configurable distance and time threshold
- Multi-camera support with camera selector dropdown
- Support for both live webcam and recorded CCTV video files
- Visual alerts with red bounding box and warning message
- Alert history page with full detection log
- Operator acknowledgement and alert reset feature
- Secure login with username and password
- Standalone Windows EXE requiring no installation

---

## 🖥️ Application Screenshots

### Login Screen
> Secure login page for authorized personnel only

### Main Dashboard
> Live camera feed with real-time detection and alert panel

### Alert History
> Complete log of all past detections with timestamp, object type, camera source, and status

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.13 | Core programming language |
| YOLOv8s | Real-time object detection |
| OpenCV | Video frame processing |
| PyQt5 | Desktop GUI framework |
| PyTorch | Deep learning backend |
| PyInstaller | Windows EXE packaging |

---

## 📁 Project Structure

```
VigiLens/
├── assets/
├── gui/
│   ├── __init__.py
│   ├── login_window.py
│   └── dashboard_window.py
├── alert.py
├── detection.py
├── main.py
├── ownership.py
├── requirements.txt
└── yolov8s.pt
```

---

## ⚙️ Installation and Setup

**Step 1 — Clone the repository**
```
git clone https://github.com/reddykr69/VigiLens.git
cd VigiLens
```

**Step 2 — Create virtual environment**
```
python -m venv venv
venv\Scripts\activate
```

**Step 3 — Install dependencies**
```
pip install -r requirements.txt
```

**Step 4 — Run the application**
```
python main.py
```

---

## 🔐 Login Credentials

| Field | Value |
|---|---|
| Username | admin |
| Password | vigil123 |

---

## 🔄 How It Works

1. The system captures video frames from a selected camera or video file using OpenCV
2. Each frame is processed through YOLOv8s to detect persons and bag-type objects
3. The ownership association module links each detected object to its nearest person
4. The system monitors the distance between each object and its owner continuously
5. If the owner moves beyond the distance threshold and the object remains stationary for 10 seconds the system triggers an alert
6. A red bounding box is drawn around the abandoned object and a log entry is recorded in the alert history

---

## 📊 Supported Object Classes

- Person
- Backpack
- Handbag
- Suitcase

---

## 🔮 Future Improvements

- SQLite database integration for persistent alert history
- Email notification on alert trigger
- Multi-camera grid view
- Mobile application using TensorFlow Lite
- Cloud deployment support
- Role-based user management

---

## 📄 Patent

This project has been filed for a provisional patent under the title:

**VigiLens: A Real-Time Video Surveillance System for Detection of Abandoned Objects**

---

## 🏫 Academic Details

- Project Type: Final Year Project
- Domain: Artificial Intelligence and Deep Learning
- Academic Year: 2025-2026

---

## 👨‍💻 Developer

**Rupesh**
- GitHub: [@reddykr69](https://github.com/reddykr69)

---

## 📜 License

This project is licensed under the MIT License.

---

> VigiLens — Intelligent Vision for Safer Spaces
