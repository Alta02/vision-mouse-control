import cv2
import mediapipe as mp
import pyautogui

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

    if hands:
        for hand in hands:
            # Draw hand landmarks on the frame
            drawing_utils.draw_landmarks(frame, hand)
            
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                # Convert normalized coordinates to pixel values
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                
                if id == 12:  # Middle finger tip
                    # Draw a circle at the middle finger tip
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    
                    # Map middle finger coordinates to screen coordinates
                    middle_x = screen_width / frame_width * x
                    middle_y = screen_height / frame_height * y
                    
                    # Move the mouse cursor
                    pyautogui.moveTo(middle_x, middle_y)
                
                if id == 4:  # Thumb tip
                    # Draw a circle at the thumb tip
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    
                    # Map thumb coordinates to screen coordinates
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y
                    
                    # Print the distance between middle finger and thumb
                    # print("Distance between middle finger and thumb:", abs(middle_y - thumb_y))
                    
                    # Perform a click if the middle finger and thumb are close
                    if abs(middle_y - thumb_y) < 20:
                        pyautogui.click()
                        pyautogui.sleep(1)  # Sleep to prevent multiple clicks

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