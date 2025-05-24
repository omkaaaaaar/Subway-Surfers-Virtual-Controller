import cv2
import mediapipe as mp
from pynput.keyboard import Controller as KeyboardController, Key
from pynput.mouse import Controller as MouseController, Button
import time
import math

# Setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.85,
    min_tracking_confidence=0.85
)

keyboard = KeyboardController()
mouse = MouseController()
cap = cv2.VideoCapture(0)

cooldown = 1
gesture_hold_time = 0.3
last_action_time = 0
gesture_start_time = {}

# Gesture helpers
def calc_distance(p1, p2):
    return math.hypot(p1.x - p2.x, p1.y - p2.y)

def is_hand_open(landmarks):
    return (landmarks[8].y < landmarks[6].y and
            landmarks[12].y < landmarks[10].y and
            landmarks[16].y < landmarks[14].y and
            landmarks[20].y < landmarks[18].y)

def is_peace_sign(landmarks):
    return (landmarks[8].y < landmarks[6].y and
            landmarks[12].y < landmarks[10].y and
            landmarks[16].y > landmarks[14].y and
            landmarks[20].y > landmarks[18].y)

def is_index_up(landmarks):
    return (landmarks[8].y < landmarks[6].y and
            landmarks[12].y > landmarks[10].y and
            landmarks[16].y > landmarks[14].y and
            landmarks[20].y > landmarks[18].y)

def is_ok_sign(landmarks):
    return calc_distance(landmarks[4], landmarks[8]) < 0.05

def is_fist(landmarks):
    return (landmarks[8].y > landmarks[6].y and
            landmarks[12].y > landmarks[10].y and
            landmarks[16].y > landmarks[14].y and
            landmarks[20].y > landmarks[18].y)

# Main loop
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    current_time = time.time()

    gestures = {}

    if result.multi_hand_landmarks and result.multi_handedness:
        for hand_landmarks, hand_info in zip(result.multi_hand_landmarks, result.multi_handedness):
            label = hand_info.classification[0].label  # "Left" or "Right"
            landmarks = hand_landmarks.landmark
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            if is_fist(landmarks):
                gestures[label] = 'fist'
            elif is_ok_sign(landmarks):
                gestures[label] = 'mouse_click'
            elif is_peace_sign(landmarks):
                gestures[label] = 'jump'  # ✌️ now jump
            elif is_index_up(landmarks):
                gestures[label] = 'slide'  # ☝️ now slide
            elif is_hand_open(landmarks):
                gestures[label] = 'left' if label == "Left" else 'right'

        # If both fists, do nothing
        if gestures.get("Left") == 'fist' and gestures.get("Right") == 'fist':
            cv2.putText(frame, "✊✊ Both fists - No Action", (30, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        else:
            for label, gesture in gestures.items():
                # Skip if this hand is a fist
                if gesture == 'fist':
                    continue

                # Allow gesture if other hand is a fist
                other_label = "Right" if label == "Left" else "Left"
                if other_label in gestures and gestures[other_label] == 'fist':
                    pass

                if gesture not in gesture_start_time:
                    gesture_start_time[gesture] = current_time
                elif current_time - gesture_start_time[gesture] > gesture_hold_time and current_time - last_action_time > cooldown:
                    if gesture == 'slide':
                        print("☝️ Index finger → Slide")
                        keyboard.press(Key.down)
                        keyboard.release(Key.down)
                    elif gesture == 'jump':
                        print("✌️ Peace sign → Jump")
                        keyboard.press(Key.up)
                        keyboard.release(Key.up)
                    elif gesture == 'left':
                        print("✋ Left palm → Move Left")
                        keyboard.press(Key.left)
                        keyboard.release(Key.left)
                    elif gesture == 'right':
                        print("🤚 Right palm → Move Right")
                        keyboard.press(Key.right)
                        keyboard.release(Key.right)
                    elif gesture == 'mouse_click':
                        print("👌 OK sign → Mouse Click")
                        mouse.click(Button.left, 1)

                    last_action_time = current_time
                    gesture_start_time = {}
    else:
        gesture_start_time = {}

    cv2.imshow("Subway Surfer Controller", frame)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
