import cv2
import numpy as np
import os
import mediapipe as mp

# Initialize mediapipe utilities for drawing and hand detection
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# Perform mediapipe detection on an image using a specified model
def mediapipe_detection(image, model):
    if image is None:
        raise ValueError("Input image cannot be None")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert color for mediapipe
    image.flags.writeable = False  # Improve performance by disabling write access
    results = model.process(image)  # Process the image to detect hands
    image.flags.writeable = True  # Re-enable write access to the image
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Convert back to BGR for OpenCV
    return image, results  # Return the processed image and detection results

# Draw landmarks and hand connections on the image
def draw_styled_landmarks(image, results):
    if results is None:
        return image
    if hasattr(results, 'multi_hand_landmarks') and results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
    return image