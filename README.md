# 🚗 Drowsiness Detection System

A real-time **Driver Drowsiness Detection System** built using **Flask**, **MediaPipe**, **OpenCV**, and **Pygame**.  
The system uses the laptop's webcam to detect a person’s eye aspect ratio (EAR) and alerts the driver if drowsiness is detected.

---

## 🧠 Features

- 👁️ Real-time face and eye detection using **MediaPipe Face Mesh**
- ⚙️ Computes **Eye Aspect Ratio (EAR)** to determine drowsiness
- 🔔 Plays an alarm sound when drowsiness is detected
- 🌐 Simple web interface for camera preview and detection feedback
- 📊 Real-time EAR monitoring

---

## 🗂️ Project Structure

drowsiness_detection/
│
├── app.py # Main Flask application
├── requirements.txt # Python dependencies
├── alarm.wav # Alarm sound file
│
├── templates/
│ └── index.html # Webpage with camera stream
│
└── static/
└── (optional) # For future CSS/JS or assets


---

## 🧩 Requirements

Make sure you have **Python 3.10+** installed.  
Then, create and activate a virtual environment:

##bash
python -m venv .venv
.venv\Scripts\activate     # for Windows
# or
source .venv/bin/activate  # for Mac/Linux

⚠️ Notes

Works best in well-lit environments

May require adjusting EAR threshold in app.py:

EAR_THRESHOLD = 0.22
CONSEC_FRAMES = 15
Lowering the threshold makes detection more sensitive.

🧑‍💻 Technologies Used

Python
Flask
OpenCV
MediaPipe
Pygame
Socket.IO (WebSocket communication)

##📸 Output Preview

✅ Detects open/closed eyes in real time

🚨 Plays an alarm when the user appears drowsy

🖥️ Displays EAR (Eye Aspect Ratio) values on the web interface
