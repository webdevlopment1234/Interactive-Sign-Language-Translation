import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow logging

import tensorflow as tf
# Configure GPU Memory Growth
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print("GPU Memory Growth Enabled")
    except RuntimeError as e:
        print(f"GPU Error: {e}")

from flask import Flask, render_template, Response, jsonify
from function import *
from keras.models import model_from_json
import cv2
import numpy as np
import logging
from waitress import serve

# Disable flask logging for polling endpoint
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__, static_folder='frontend/dist', static_url_path='/static', template_folder='frontend/dist')

# Load model
json_file = open("model.json", "r")
model_json = json_file.read()
json_file.close()
model = model_from_json(model_json)
model.load_weights("model.h5")

# Detection variables
sequence = []
sentence = []
accuracy = []
predictions = []
threshold = 0.8

def generate_frames():
    global sequence, sentence, accuracy, predictions
    cap = cv2.VideoCapture(0)
    
    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
        
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break
            
            cropframe = frame[40:400, 0:300]
            cv2.rectangle(frame, (0, 40), (300, 400), (245, 117, 16), 2)
            
            image, results = mediapipe_detection(cropframe, hands)
            keypoints = extract_keypoints(results)
            sequence.append(keypoints)
            sequence = sequence[-30:]
            
            try:
                if len(sequence) == 30:
                    with tf.device('/GPU:0' if gpus else '/CPU:0'):
                        res = model.predict(np.expand_dims(sequence, axis=0), verbose=0)[0]
                    
                    predictions.append(np.argmax(res))
                    current_predictions = predictions[-10:]
                    
                    if len(current_predictions) >= 10:
                        unique_preds = np.unique(current_predictions)
                        if len(unique_preds) == 1 and unique_preds[0] == np.argmax(res):
                            if res[np.argmax(res)] > threshold:
                                predicted_action = actions[np.argmax(res)]
                                if not sentence or predicted_action != sentence[-1]:
                                    sentence.append(predicted_action)
                                    accuracy.append(f"{res[np.argmax(res)] * 100:.2f}%")
                    
                    if len(sentence) > 5:
                        sentence, accuracy = sentence[-5:], accuracy[-5:]
            except Exception as e:
                print(f"Prediction Error: {e}")
            
            # UI Overlay
            cv2.rectangle(frame, (0, 0), (300, 40), (245, 117, 16), -1)
            output_text = "Output: " + (" ".join(sentence) if sentence else "None")
            if accuracy: output_text += f" ({accuracy[-1]})"
            cv2.putText(frame, output_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
            
            ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
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
        'accuracy': accuracy[-1] if accuracy else "0%"
    })

@app.route('/api/actions')
def get_actions():
    return jsonify(list(actions))

if __name__ == "__main__":
    print("\n" + "="*50)
    print("SERVE RUNNING AT: http://127.0.0.1:5000")
    print("="*50 + "\n")
    serve(app, host='127.0.0.1', port=5000, threads=6)
