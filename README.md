🎮 Gesture-Controlled Media Player using Python, OpenCV & Mediapipe

Control your media player with simple hand gestures — no keyboard, no mouse, just your webcam and Python magic!
This project uses real-time hand tracking to map different finger gestures to media control actions like play/pause, mute, volume up/down, and next/previous.


🧠 Features:

👋 Hand gesture recognition using Mediapipe
🎯 Stable gesture detection using a sliding buffer
🖥️ Media control via PyAutoGUI (compatible with VLC, YouTube, etc.)
✅ Both left & right hands supported
👀 Visual hand landmarks feedback
📊 Live FPS display & gesture label

✋ Gesture Mappings:

5 Fingers (Open Palm)	   ▶️⏸️ Play / Pause
0 Fingers (Fist)	       🔇 Mute
1 Finger (Index)	       ⏮️ Previous
2 Fingers (Index+Middle) ⏭️ Next
3 Fingers	               🔊 Volume Up
4 Fingers	               🔉 Volume Down



📁 Usage:

Run the script: python gestures.py
Then perform the hand gestures in front of your webcam.
Press Q to quit the application.

🤖 Tech Stack:

Python — core language
OpenCV — video stream handling and UI
MediaPipe — hand tracking with landmark detection
PyAutoGUI — keyboard control for media
Deque — stability buffer for consistent gesture detection

💡 Known Limitations
Lighting and hand visibility affect accuracy
Fast or partial gestures may not register
Currently rule-based; could be upgraded with ML in future
