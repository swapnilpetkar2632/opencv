
import cv2
import mediapipe as mp
import time
from pynput.keyboard import Key, Controller

# --- Setup Keyboard Controller ---
keyboard = Controller()

# --- Setup MediaPipe ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1, # Only track one hand
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# --- Setup Webcam ---
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# --- Variables for Gesture Logic ---
prev_x = 0               # Stores the last x-position of the index finger
last_action_time = 0     # Timestamp of the last action
COOLDOWN_SECONDS = 1.0   # 1 second cooldown
SWIPE_THRESHOLD = 0.08   # How far (as a percentage of screen width) you need to move

print("Starting webcam... Swipe your index finger left to press the LEFT arrow key.")
print("Press 'q' to quit.")

# --- Main Loop ---
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        continue

    # Flip the frame, convert to RGB
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame
    results = hands.process(rgb_frame)

    # --- Gesture Logic ---
    if results.multi_hand_landmarks:
        # Get landmarks for the first hand
        hand_landmarks = results.multi_hand_landmarks[0]
        
        # Get the coordinate for the Index Finger Tip (Landmark 8)
        index_tip = hand_landmarks.landmark[8]
        current_x = index_tip.x
        
        # Check if this is the first frame with a hand
        if prev_x == 0:
            prev_x = current_x # Initialize prev_x

        # Calculate movement
        delta_x = current_x - prev_x
        current_time = time.time()

        # Check for cooldown
        if (current_time - last_action_time) > COOLDOWN_SECONDS:
            
            # --- ACTION: SWIPE LEFT ---
            # (delta_x is negative because x-values decrease to the left)
            if delta_x < -SWIPE_THRESHOLD:
                print(f"SWIPE LEFT DETECTED! (Movement: {delta_x:.2f})")
                print(">>> Pressing LEFT Arrow Key")
                
                # --- This is the command ---
                keyboard.press(Key.left)
                keyboard.release(Key.left)
                # -------------------------
                
                last_action_time = current_time # Start cooldown
                
            # --- ACTION: SWIPE RIGHT ---
            elif delta_x > SWIPE_THRESHOLD:
                print(f"SWIPE RIGHT DETECTED! (Movement: {delta_x:.2f})")
                print(">>> Pressing RIGHT Arrow Key")
                
                # --- This is the command ---
                keyboard.press(Key.right)
                keyboard.release(Key.right)
                # -------------------------
                
                last_action_time = current_time # Start cooldown

        # Update prev_x for the next frame
        prev_x = current_x
        
        # Draw the landmarks on the frame
        mp_drawing.draw_landmarks(
            frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    
    else:
        # If no hand is detected, reset prev_x
        prev_x = 0

    # Display the frame
    cv2.imshow('Gesture Control', frame)

    # Exit on 'q'
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# --- Cleanup ---
cap.release()
cv2.destroyAllWindows()  
