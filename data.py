from function import *  # Import custom functions for mediapipe operations
from time import sleep
import cv2

# Create directories for storing frames of each action sequence
try:
    for action in actions:
        for sequence in range(no_sequences):
            os.makedirs(os.path.join(DATA_PATH, action, str(sequence)), exist_ok=True)
    print(f"Successfully created directories for {len(actions)} actions")
except Exception as e:
    print(f"Error creating directories: {e}")
    exit(1)

# Initialize mediapipe for hand detection
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.3,  # Lower confidence for more hand captures
    min_tracking_confidence=0.3) as hands:

    # Loop through each action, sequence, and frame to capture data
    for action in actions:
        for sequence in range(no_sequences):
            for frame_num in range(sequence_length):
                image_path = f'Image/{action}/{frame_num}.png'
                frame = cv2.imread(image_path)  # Load each frame image
                if frame is None:
                    print(f"Warning: Image not found at {image_path} for {action} sequence {sequence}")
                    continue

                try:
                    # Run hand detection on the frame
                    image, results = mediapipe_detection(frame, hands)
                    
                    # Check for hand detection and print status
                    if results.multi_hand_landmarks:
                        print(f"Hand detected for {action} sequence {sequence}, frame {frame_num}")
                    else:
                        print(f"No hand detected for {action} sequence {sequence}, frame {frame_num}")
                except Exception as e:
                    print(f"Error processing frame {frame_num} for {action} sequence {sequence}: {e}")
                    continue

                try:
                    draw_styled_landmarks(image, results)  # Draw hand landmarks if detected

                    # Display the collection status
                    message = f"Collecting frames for {action} Video {sequence}"
                    cv2.putText(image, message, (15, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                    cv2.imshow('OpenCV Feed', image)
                except Exception as e:
                    print(f"Error displaying frame for {action} sequence {sequence}: {e}")

                try:
                    # Extract and save keypoints
                    keypoints = extract_keypoints(results)
                    npy_path = os.path.join(DATA_PATH, action, str(sequence), str(frame_num))
                    np.save(npy_path, keypoints)  # Save keypoints to .npy file
                    print(f"Saved keypoints to {npy_path}")
                except Exception as e:
                    print(f"Error saving keypoints for {action} sequence {sequence}, frame {frame_num}: {e}")

                try:
                    if cv2.waitKey(10) & 0xFF == ord('q'):  # Press 'q' to exit
                        print("User interrupted data collection")
                        break
                except Exception as e:
                    print(f"Error handling keyboard input: {e}")
                    break

    cv2.destroyAllWindows()  # Close OpenCV window
    print("Data collection completed successfully")