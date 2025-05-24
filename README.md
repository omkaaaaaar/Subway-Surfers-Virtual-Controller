# Subway-Surfers-Virtual-Controller

🕹️ Subway Surfer Virtual Controller (Hand Gesture Recognition using OpenCV & MediaPipe)

This project implements a virtual controller for **Subway Surfers** using Python, OpenCV, and MediaPipe. By recognizing real-time hand gestures via a webcam, it allows users to control in-game actions like *jump*, *slide*, *move left/right*, and *click* — all without touching the keyboard!

# 🚀 Features

- ✋ Detects various hand gestures using **MediaPipe**
- 🎮 Maps gestures to game actions (jump, slide, left, right, click)
- 👊 Ignores unintentional actions (e.g., both fists up = pause/no action)
- 🧠 Real-time processing with **OpenCV**
- 💻 Fully built in Python, no additional hardware needed

# 🧰 Requirements

Install the following Python packages:

```bash
pip install opencv-python mediapipe pyautogui
```

> 💡 Optional: Use a virtual environment to avoid conflicts.

# ✋ Supported Gestures and Mappings

| Gesture             | Action           |
|---------------------|------------------|
| Open Palm (Left)    | Move Left        |
| Open Palm (Right)   | Move Right       |
| Peace ✌️ (Right)     | Mouse Click      |
| Index Finger Up     | Jump             |
| OK Sign             | Slide            |
| Two Fists Up        | No Action (Pause)|

# 🧪 How to Test

To test gesture detection individually:

```bash
python test.py
```

To run the actual game controller:

```bash
python subway_gesture_controller.py
```

Ensure your webcam is connected and lighting is sufficient.

# ⚙️ How It Works

1. **Webcam Feed**: Captures real-time video frames.
2. **MediaPipe Hands**: Detects hand landmarks (21 points per hand).
3. **Gesture Recognition**: Applies logic to recognize specific hand poses.
4. **Action Mapping**: Maps recognized gestures to keyboard/mouse actions using `pyautogui`.

# 🖼️ Demo

https://www.linkedin.com/feed/update/urn:li:activity:7317845483870150656/

# 📌 Notes

- This is optimized for Subway Surfers but can be adapted for other games.
- Ensure hand gestures are clearly visible to the camera.
- Adjust detection sensitivity as needed in `subway_gesture_controller.py`.

# 🧑‍💻 Author

Omkar Patkar 
Artificial Intelligence & Data Science Engineering student at Konkan Gyanpeeth College of Engineering*

