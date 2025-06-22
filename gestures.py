import cv2
import mediapipe as mp
import pyautogui
import time
from collections import deque

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.6
)
mp_draw = mp.solutions.drawing_utils
finger_tips = [4, 8, 12, 16, 20]

gesture_queue = deque(maxlen=3)
last_action_time = 0
cooldown_period = 1.0
current_gesture_label = ""
prev_time = 0

def interpret_gesture(finger_count):
    actions = {
        5: "play_pause",
        0: "mute",
        1: "prev",
        2: "next",
        3: "vol_up",
        4: "vol_down"
    }
    return actions.get(finger_count, "")

def display_text(frame, text, position, size=0.8, color=(255, 255, 255)):
    cv2.putText(frame, text, position, cv2.FONT_HERSHEY_DUPLEX, size, color, 2)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    detected_gesture = ""

    if results.multi_hand_landmarks:
        lm_points = []
        hand = results.multi_hand_landmarks[0]
        for lm in hand.landmark:
            x, y = int(lm.x * w), int(lm.y * h)
            lm_points.append((x, y))

        handedness = results.multi_handedness[0].classification[0].label
        fingers = []

        if handedness == "Right":
            fingers.append(int(lm_points[finger_tips[0]][0] < lm_points[finger_tips[0] - 1][0]))
        else:
            fingers.append(int(lm_points[finger_tips[0]][0] > lm_points[finger_tips[0] - 1][0]))

        for tip_id in finger_tips[1:]:
            fingers.append(int(lm_points[tip_id][1] < lm_points[tip_id - 2][1]))

        count = sum(fingers)
        detected_gesture = interpret_gesture(count)
        gesture_queue.append(detected_gesture)

        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

    if (
        len(set(gesture_queue)) == 1 and
        detected_gesture and
        time.time() - last_action_time > cooldown_period
    ):
        action = gesture_queue[-1]
        if action == "play_pause":
            pyautogui.press("space")
            current_gesture_label = "Play / Pause"
        elif action == "mute":
            pyautogui.press("m")
            current_gesture_label = "Mute"
        elif action == "next":
            pyautogui.press("right")
            current_gesture_label = "Next"
        elif action == "prev":
            pyautogui.press("left")
            current_gesture_label = "Previous"
        elif action == "vol_up":
            pyautogui.press("volumeup")
            current_gesture_label = "Volume Up"
        elif action == "vol_down":
            pyautogui.press("volumedown")
            current_gesture_label = "   Volume Down"

        last_action_time = time.time()

    if detected_gesture:
        display_text(frame, f"Gesture: {current_gesture_label}", (10, h - 30), 0.8, (0, 255, 0))

    curr_time = time.time()
    fps = int(1 / (curr_time - prev_time)) if prev_time != 0 else 0
    prev_time = curr_time
    display_text(frame, f"FPS: {fps}", (10, 25), 0.6, (100, 255, 100))
    display_text(frame, "Press Q to Quit", (10, 55), 0.5, (180, 180, 180))

    cv2.imshow("Gesture Media Controller", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
