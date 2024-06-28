import cv2
import mediapipe as mp
import pyautogui

#collider
def isColliding(a_xys: tuple, b_xys: tuple, xy: tuple = None) -> bool:
    ax, ay, a_size = a_xys
    bx, by, b_size = b_xys
    
    # Calculate boundaries of both rectangles
    a_left = ax - (a_size / 2)
    a_right = ax + (a_size / 2)
    a_top = ay - (a_size / 2)
    a_bottom = ay + (a_size / 2)
    
    b_left = bx - (b_size / 2)
    b_right = bx + (b_size / 2)
    b_top = by - (b_size / 2)
    b_bottom = by + (b_size / 2)
    
    # Check for collision when touching
    touching_condition = ((a_right >= b_left and a_left <= b_right) or (a_bottom >= b_top and a_top <= b_bottom))
    
    return touching_condition

# Switcher variables
cam = 0

def switch_cam(reset=False):
    global cam, cap

    cam = cam + 1 if not reset else 0
    cap.release()
    cap = initialize_camera(cam)

# Function to initialize webcam
def initialize_camera(cam_index):
    cap = cv2.VideoCapture(cam_index)
    return cap

# Initialize webcam
cap = initialize_camera(cam)

# Initialize MediaPipe Hand Detector
hand_detector = mp.solutions.hands.Hands()

# Initialize MediaPipe Drawing Utils
drawing_utils = mp.solutions.drawing_utils

# Get screen size
screen_width, screen_height = pyautogui.size()

middle_y = 0  # Initialize middle finger y-coordinate

# Initialize coordinates with default values
middle_x = 0
middle_y = 0
thumb_x = 0
indexF_x = 0

while True:
    # Capture frame from webcam
    _, frame = cap.read()
    
    # Flip the frame horizontally for natural hand movement
    frame = cv2.flip(frame, 1)
    
    # Get frame dimensions
    try:
        frame_height, frame_width, _ = frame.shape
    except AttributeError:
        switch_cam(reset=True)
        continue
    
    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the RGB frame to detect hands
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    # Reset coordinates if no hands are detected
    if not hands:
        middle_x = 0
        middle_y = 0
        thumb_x = 0
        indexF_x = 0

    if hands:
        for hand in hands:
            # Draw hand landmarks on the frame
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                # Convert normalized coordinates to pixel values
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                if id == 8: #index finger
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 34))
                    indexF_x = screen_width / frame_width * x
                    indexF_y = screen_height / frame_height * y
                    pyautogui.moveTo(indexF_x, indexF_y)

                if id == 12:  # Middle finger tip
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 155, 165))
                    middle_x = screen_width / frame_width * x
                    middle_y = screen_height / frame_height * y
                
                if id == 4:  # Thumb tip
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255)) #make it 20, thumb's bigger
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y

                    # Perform a click if the middle finger and thumb are close
                    if thumb_x and middle_x and indexF_x:
                        if isColliding(a_xys=(middle_x, middle_y, 10), b_xys=(thumb_x, thumb_y, 20)):
                            pyautogui.mouseDown()
                        elif isColliding(a_xys=(indexF_x, indexF_y, 10), b_xys=(thumb_x, thumb_y, 20)):
                            pyautogui.click()
                            pyautogui.sleep(1)
                        else:
                            pyautogui.mouseUp()

    # Display the frame
    cv2.imshow("Hand Gesture Mouse Control", frame)
    
    # Exit the loop if 'q' is pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        switch_cam()
        print(f"Switched to camera {cam}")

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()