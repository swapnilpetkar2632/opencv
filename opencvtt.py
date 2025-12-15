# test_opencv.py
import cv2
import mediapipe as mp

print("OpenCV version:", cv2.__version__)
print("MediaPipe version:", mp.__version__)

# Test webcam
cap = cv2.VideoCapture(0)
if cap.isOpened():
    print("Webcam working!")
    cap.release()
else:
    print("Webcam not available")