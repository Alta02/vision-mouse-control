
# Hand Gesture Mouse Control

  

This project allows you to control your mouse using hand gestures. It uses OpenCV for video capture, MediaPipe for hand detection, and PyAutoGUI for mouse control.

  

## Requirements

  

- Python 3.12.3

- OpenCV

- MediaPipe

- PyAutoGUI

  

### Installation

1. Clone the repository

```bash
git  clone  https://github.com/Alta02/vision-mouse-control.git
```

  

2. Navigate to the directory

```bash
cd  vision-mouse-control
```

3. Install the required libraries

```bash
pip  install  -r  requirements.txt
```

**note:** this method has error potentials. if error happened while installing, try this one instead :

```bash
pip  install  opencv-python  mediapipe  pyautogui
```

  
  

### Usage

1. Make sure your webcam is connected and functioning.

  

2. Run the script using Python:

```powershell
python mouse_control.py
```

3. The script will open a window displaying the webcam feed. Use the following gestures to control the mouse:


- Move your middle finger (ID 12) to move the mouse cursor.

- Move your thumb (ID 4) close to your index finger to perform a mouse click.

- Press `s` to change webcam

- Press `q` to exit the application.

- Enjoy