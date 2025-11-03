import cv2
import numpy as np
import mediapipe as mp
import pygame
import threading
from flask import Flask, render_template, Response

# Initialize Flask
app = Flask(__name__)

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Initialize Pygame for alarm
pygame.mixer.init()
pygame.mixer.music.load("alarm.wav")  # Make sure alarm.wav is valid and in same folder

# Alarm control
alarm_playing = False

def play_alarm():
    """Play alarm sound in a separate thread."""
    global alarm_playing
    if not alarm_playing:
        alarm_playing = True
        pygame.mixer.music.play(-1)  # Loop alarm

def stop_alarm():
    """Stop alarm."""
    global alarm_playing
    if alarm_playing:
        pygame.mixer.music.stop()
        alarm_playing = False

def eye_aspect_ratio(landmarks, eye_indices):
    """Calculate the Eye Aspect Ratio (EAR)."""
    points = np.array([(landmarks[i].x, landmarks[i].y) for i in eye_indices])
    A = np.linalg.norm(points[1] - points[5])
    B = np.linalg.norm(points[2] - points[4])
    C = np.linalg.norm(points[0] - points[3])
    ear = (A + B) / (2.0 * C)
    return ear

def generate_frames():
    """Capture video, detect drowsiness, show results."""
    cap = cv2.VideoCapture(0)
    global alarm_playing

    LEFT_EYE = [33, 160, 158, 133, 153, 144]
    RIGHT_EYE = [362, 385, 387, 263, 373, 380]
    EAR_THRESHOLD = 0.25
    CONSEC_FRAMES = 15
    frame_count = 0

    while True:
        success, frame = cap.read()
        if not success:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                left_ear = eye_aspect_ratio(face_landmarks.landmark, LEFT_EYE)
                right_ear = eye_aspect_ratio(face_landmarks.landmark, RIGHT_EYE)
                ear = (left_ear + right_ear) / 2.0

                # Draw EAR on screen
                cv2.putText(frame, f"EAR: {ear:.2f}", (30, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # Check drowsiness
                if ear < EAR_THRESHOLD:
                    frame_count += 1
                    if frame_count >= CONSEC_FRAMES:
                        cv2.putText(frame, "🚨 DROWSINESS DETECTED 🚨", (100, 100),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 0, 255), 3)
                        # Flash red overlay
                        overlay = frame.copy()
                        overlay[:] = (0, 0, 255)
                        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
                        threading.Thread(target=play_alarm).start()
                else:
                    frame_count = 0
                    stop_alarm()
        else:
            stop_alarm()
            frame_count = 0
            cv2.putText(frame, "No face detected", (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        # Encode and stream
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    print("🚗 Starting Drowsiness Detection System...")
    app.run(host="127.0.0.1", port=5000, debug=True)
