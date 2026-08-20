import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow logging

try:
    import tensorflow as tf
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            print("GPU Memory Growth Enabled")
        except RuntimeError as e:
            print("GPU Error: %s" % e)
except Exception as e:
    print("TensorFlow import error: %s" % e)
    tf = None

import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)

import json
import numpy as np
import cv2
import logging
from pathlib import Path

from flask import Flask, render_template, Response, jsonify
from function import mp_drawing, mp_drawing_styles, mp_hands, mediapipe_detection, draw_styled_landmarks
from waitress import serve

# Disable flask logging for polling endpoint
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIST = BASE_DIR / "frontend" / "dist"

app = Flask(
    __name__,
    static_folder=str(FRONTEND_DIST),
    static_url_path='/static',
    template_folder=str(FRONTEND_DIST),
)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Never cache static files (avoid stale bundle after rebuilds)

# --- Load CNN model ----------------------------------------------------------
from tensorflow.keras.models import load_model
model = load_model(BASE_DIR / "model_cnn.h5", compile=False)


# Load label map dynamically -- no hardcoded letters
with open(BASE_DIR / "model_cnn_labels.json", "r") as f:
    raw_map = json.load(f)
# Keys are strings in JSON; convert to int for indexing
label_map = {int(k): v for k, v in raw_map.items()}
num_classes = len(label_map)
print("CNN model loaded. Classes: %s" % [label_map[i] for i in sorted(label_map)])

# --- Detection variables -----------------------------------------------------
sentence = []
accuracy = []
predictions = []
threshold = 0.6
current_action = "None"
current_confidence = "0%"

IMG_SIZE = 28  # CNN expects 28x28 grayscale


def preprocess_roi(roi):
    """Convert a BGR camera ROI to 28x28 grayscale normalized array for the CNN."""
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (IMG_SIZE, IMG_SIZE))
    normalized = resized.astype('float32') / 255.0
    return normalized.reshape(1, IMG_SIZE, IMG_SIZE, 1)


def generate_frames():
    global sentence, accuracy, predictions, current_action, current_confidence

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("CRITICAL: Camera could not be opened.")
        return

    MIRROR_DISPLAY = False

    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:

        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            # Detection ROI (same region as before)
            detection_roi = frame[40:400, 0:300].copy()

            # Draw ROI rectangle
            cv2.rectangle(frame, (0, 40), (300, 400), (245, 117, 16), 2)

            # Run MediaPipe for landmark drawing only
            image, results = mediapipe_detection(detection_roi, hands)
            image = draw_styled_landmarks(image, results)
            frame[40:400, 0:300] = image

            if results.multi_hand_landmarks:
                try:
                    # Get hand bounding box from landmarks for tighter crop
                    h, w = detection_roi.shape[:2]
                    hand_lms = results.multi_hand_landmarks[0].landmark
                    xs = [lm.x for lm in hand_lms]
                    ys = [lm.y for lm in hand_lms]

                    pad = 0.15  # padding fraction
                    x1 = max(0, int((min(xs) - pad) * w))
                    x2 = min(w, int((max(xs) + pad) * w))
                    y1 = max(0, int((min(ys) - pad) * h))
                    y2 = min(h, int((max(ys) + pad) * h))

                    hand_crop = detection_roi[y1:y2, x1:x2]

                    if hand_crop.size == 0:
                        hand_crop = detection_roi  # fall back to full ROI

                    # Preprocess and predict
                    cnn_input = preprocess_roi(hand_crop)
                    res = model.predict(cnn_input, verbose=0)[0]
                    predicted_idx = int(np.argmax(res))
                    confidence_val = float(res[predicted_idx])

                    current_action = label_map[predicted_idx]
                    current_confidence = "%.1f%%" % (confidence_val * 100)

                    predictions.append(predicted_idx)
                    current_predictions = predictions[-10:]

                    print("Detected: %s (%s)    " % (current_action, current_confidence), end='\r')

                    if len(current_predictions) >= 10:
                        unique_preds = np.unique(current_predictions)
                        if len(unique_preds) == 1 and unique_preds[0] == predicted_idx:
                            if confidence_val > threshold:
                                predicted_action = label_map[predicted_idx]
                                if not sentence or predicted_action != sentence[-1]:
                                    sentence.append(predicted_action)
                                    accuracy.append(current_confidence)
                                    print("\nACTION CONFIRMED: %s!!" % predicted_action)

                    if len(sentence) > 5:
                        sentence, accuracy = sentence[-5:], accuracy[-5:]

                except Exception as e:
                    print("\nPrediction Error: %s" % e)
            else:
                predictions = []
                current_action = "Waiting..."
                current_confidence = "-"

            display_frame = frame
            if MIRROR_DISPLAY:
                display_frame = cv2.flip(frame, 1)

            # UI Overlay
            cv2.rectangle(display_frame, (0, 0), (640, 40), (245, 117, 16), -1)
            sentence_str = "Sentence: " + (" ".join(sentence) if sentence else "...")
            cv2.putText(display_frame, sentence_str, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

            if accuracy:
                acc_text = "Acc: %s" % accuracy[-1]
                cv2.putText(display_frame, acc_text, (500, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

            ret, buffer = cv2.imencode('.jpg', display_frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    cap.release()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/get_prediction')
def get_prediction():
    return jsonify({
        'sentence': " ".join(sentence) if sentence else "None",
        'accuracy': accuracy[-1] if accuracy else "0%",
        'current_action': current_action,
        'current_confidence': current_confidence
    })


@app.route('/api/reset', methods=['POST'])
def reset_state():
    global sentence, accuracy, predictions, current_action, current_confidence
    sentence = []
    accuracy = []
    predictions = []
    current_action = "None"
    current_confidence = "0%"
    return jsonify({'status': 'success', 'message': 'State reset'})


@app.route('/api/actions')
def get_actions():
    # Return characters in model output order -- fully dynamic
    return jsonify([label_map[i] for i in sorted(label_map)])


if __name__ == "__main__":
    print("\n" + "="*50)
    print("SIGN LANGUAGE INTERPRETER RUNNING (CNN Model)")
    print("Access at: http://127.0.0.1:5000")
    print("="*50 + "\n")
    serve(app, host='127.0.0.1', port=5000, threads=6)
