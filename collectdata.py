import os
import cv2

# Start video capture from the default camera (0 represents the first camera device)
try:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit(1)
except Exception as e:
    print(f"Error initializing camera: {e}")
    exit(1)

# Directory where images for each letter are saved
directory = 'Image/'

# Continuously capture frames from the webcam
while True:
    ret, frame = cap.read()  # Read a frame from the video capture object
    if not ret:
        print("Error: Could not read frame from camera.")
        continue

    # Dictionary to count the number of images in each letter subdirectory
    try:
        count = {
            'a': len(os.listdir(directory + "/A")),
            'b': len(os.listdir(directory + "/B")),
            'c': len(os.listdir(directory + "/C")),
            '0': len(os.listdir(directory + "/0")),
            '1': len(os.listdir(directory + "/1")),
            '2': len(os.listdir(directory + "/2")),
            '3': len(os.listdir(directory + "/3")),
            '4': len(os.listdir(directory + "/4")),
            '5': len(os.listdir(directory + "/5")),
            '6': len(os.listdir(directory + "/6")),
            '7': len(os.listdir(directory + "/7")),
            '8': len(os.listdir(directory + "/8")),
            '9': len(os.listdir(directory + "/9")),
        }
    except FileNotFoundError as e:
        print(f"Directory not found: {e}")
        # Create directories if they don't exist
        for dir_name in ['A', 'B', 'C', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            os.makedirs(os.path.join(directory, dir_name), exist_ok=True)
        count = {k: 0 for k in ['a', 'b', 'c', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']}

    # Get dimensions of the captured frame
    row = frame.shape[1]
    col = frame.shape[0]

    # Draw a white rectangle on the frame to mark the Region of Interest (ROI)
    cv2.rectangle(frame, (0, 40), (300, 400), (255, 255, 255), 2)

    # Display the main capture window and the ROI window
    cv2.imshow("data", frame)
    cv2.imshow("ROI", frame[40:400, 0:300])

    # Crop the frame to show only the ROI area
    frame = frame[40:400, 0:300]

    # Check for key press to save the frame to corresponding letter folders
    interrupt = cv2.waitKey(10)
    if interrupt & 0xFF == ord('a'):
        cv2.imwrite(os.path.join(directory, 'A', f"{count['a']}.png"), frame)
    elif interrupt & 0xFF == ord('b'):
        cv2.imwrite(os.path.join(directory, 'B', f"{count['b']}.png"), frame)
    elif interrupt & 0xFF == ord('c'):
        cv2.imwrite(os.path.join(directory, 'C', f"{count['c']}.png"), frame)
    elif interrupt & 0xFF == ord('0'):
        cv2.imwrite(directory + '0/' + str(count['0']) + '.png', frame)
    elif interrupt & 0xFF == ord('1'):
        cv2.imwrite(directory + '1/' + str(count['1']) + '.png', frame)
    elif interrupt & 0xFF == ord('2'):
        cv2.imwrite(directory + '2/' + str(count['2']) + '.png', frame)
    elif interrupt & 0xFF == ord('3'):
        cv2.imwrite(directory + '3/' + str(count['3']) + '.png', frame)
    elif interrupt & 0xFF == ord('4'):
        cv2.imwrite(directory + '4/' + str(count['4']) + '.png', frame)
    elif interrupt & 0xFF == ord('5'):
        cv2.imwrite(directory + '5/' + str(count['5']) + '.png', frame)
    elif interrupt & 0xFF == ord('6'):
        cv2.imwrite(directory + '6/' + str(count['6']) + '.png', frame)
    elif interrupt & 0xFF == ord('7'):
        cv2.imwrite(directory + '7/' + str(count['7']) + '.png', frame)
    elif interrupt & 0xFF == ord('8'):
        cv2.imwrite(directory + '8/' + str(count['8']) + '.png', frame)
    elif interrupt & 0xFF == ord('9'):
        cv2.imwrite(directory + '9/' + str(count['9']) + '.png', frame) 

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()