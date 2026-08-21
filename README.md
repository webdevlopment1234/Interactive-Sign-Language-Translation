# 🤟 Real-Time Sign Language Recognition System

A deep learning-powered sign language interpreter that translates ASL hand gestures into text in real time. MediaPipe Hands tracks your hand landmarks, a lightweight CNN classifies 28×28 grayscale crops of the detected hand, and a Flask + React web app streams the results live to your browser.

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.10-FF6F00?logo=tensorflow&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Hands-0097A7)
![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-7-646CFF?logo=vite&logoColor=white)
![License](https://img.shields.io/badge/License-Academic-lightgrey)

---

## ✨ Features

- **Real-time translation** — live MJPEG video stream with per-frame inference (<100 ms latency)
- **MediaPipe Hands** — robust 21-point hand tracking with automatic bounding-box crop (15% padding)
- **CNN classifier** — 29-class model trained on the ASL alphabet dataset (28×28 grayscale input)
- **Full A–Z alphabet** — plus `del`, `space`, and `nothing` control tokens
- **Stability filtering** — a gesture is only accepted after 10 consecutive identical predictions above a 60% confidence threshold
- **Sentence builder** — confirmed gestures accumulate into a sentence (last 5 characters kept)
- **Modern web UI** — React 19 + Tailwind CSS with live feed, confidence readout, learning section, and quiz mode
- **Fully local** — all processing happens on-device; no cloud calls, no data leaves your machine

## 🏗️ System Architecture

```
┌──────────────┐    ┌───────────────────┐    ┌──────────────────────┐    ┌─────────────────┐
│  Webcam Feed │ ─▶ │  MediaPipe Hands   │ ─▶ │ Landmark-based hand  │ ─▶ │ Grayscale 28×28 │
│  (OpenCV)    │    │  landmark tracking │    │ bounding-box crop    │    │ preprocessing   │
└──────────────┘    └───────────────────┘    └──────────────────────┘    └────────┬────────┘
                                                                                 ▼
┌──────────────┐    ┌───────────────────┐    ┌──────────────────────┐    ┌─────────────────┐
│  React UI    │ ◀ │  Sentence builder  │ ◀ │ Stability filter      │ ◀ │ CNN softmax     │
│  (MJPEG +    │    │  (last 5 chars)    │    │ (10 frames @ >0.60)  │    │ prediction      │
│   polling)   │    └───────────────────┘    └──────────────────────┘    └─────────────────┘
└──────────────┘
```

**Pipeline detail:** every frame, the ROI region (`frame[40:400, 0:300]`) is scanned by MediaPipe. If a hand is found, its landmark bounding box is extracted with padding, converted to grayscale, resized to 28×28, normalized to `[0, 1]`, and fed to the CNN. Predictions are only committed to the sentence when stable.

## 🔤 Recognized Gestures (29 classes)

| Category | Labels |
|----------|--------|
| Letters | `A B C D E F G H I J K L M N O P Q R S T U V W X Y Z` |
| Control | `del` · `space` · `nothing` |

Labels are loaded dynamically from `model_cnn_labels.json` at startup — nothing is hardcoded, so retraining with new classes works out of the box.

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| Python 3.8+ | Runtime |
| TensorFlow / Keras 2.10 | CNN training & inference |
| MediaPipe | Hand landmark detection |
| OpenCV | Frame capture & image preprocessing |
| Flask + Waitress | Web server (production WSGI) |
| scikit-learn | Train/validation stratified splitting |

### Frontend
| Technology | Purpose |
|------------|---------|
| React 19 | UI framework |
| Vite 7 | Dev server & build tooling |
| Tailwind CSS 3 | Styling |
| Lucide React | Icons |

## 📁 Project Structure

```
4-yearfinalreview/
├── app.py                  # Flask backend: video streaming, inference, REST API
├── function.py             # MediaPipe detection & landmark drawing helpers
├── trainmodel_cnn.py       # CNN training script (GPU required)
├── model_cnn.h5            # Trained CNN weights
├── model_cnn.json          # Model architecture
├── model_cnn_labels.json   # Class index → label map (dynamic loading)
├── static/
│   └── archive (3)/        # ASL alphabet train/test image dataset
│       ├── asl_alphabet_train/
│       └── asl_alphabet_test/
├── Logs/cnn/               # TensorBoard training logs
└── frontend/
    ├── src/
    │   ├── App.jsx          # Layout & routing between sections
    │   ├── main.jsx         # Entry point
    │   ├── index.css        # Tailwind entry
    │   └── components/
    │       ├── Navbar.jsx       # Top navigation
    │       ├── Hero.jsx         # Landing section
    │       ├── Prediction.jsx   # Live camera feed + real-time output
    │       ├── Learning.jsx     # Alphabet learning section
    │       └── Quiz.jsx         # Practice quiz mode
    ├── dist/                # Production build (served by Flask)
    ├── vite.config.js       # Dev proxy → backend :5000
    └── package.json
```

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **Webcam**
- **NVIDIA GPU** *(only needed for training — inference runs fine on CPU)*

### 1. Clone & Set Up Python Environment

```bash
git clone <repository-url>
cd 4-yearfinalreview

python -m venv venv_new
venv_new\Scripts\activate        # Windows
# source venv_new/bin/activate   # Linux/macOS
```

### 2. Install Dependencies

```bash
pip install tensorflow==2.10.0 keras==2.10.0 mediapipe opencv-python flask waitress numpy scikit-learn
```

> ⚠️ **TensorFlow 2.10 is intentional** — it's the last native Windows build with GPU support. On Linux/macOS you may use a newer version.

### 3. Build the Frontend

```bash
cd frontend
npm install
npm run build
cd ..
```

### 4. Verify Model Files

Ensure these exist in the project root (included or produced by training):

- `model_cnn.h5` — weights
- `model_cnn.json` — architecture
- `model_cnn_labels.json` — label map

### 5. Run

```bash
python app.py
```

Open **http://127.0.0.1:5000**, click **Start Prediction**, allow camera access, and sign away.

#### Development Mode (Hot Reload)

```bash
# Terminal 1 — backend
python app.py

# Terminal 2 — frontend dev server
cd frontend && npm run dev
```

Vite serves the UI at **http://localhost:5173** and proxies `/video_feed`, `/get_prediction`, `/api/*`, and `/static/*` to the backend automatically (see `vite.config.js`).

### Using the App

1. Click **Prediction** in the navbar → **Start Prediction**
2. Place your right hand inside the orange ROI rectangle
3. Hold each sign steady for 1–2 seconds
4. Confirmed letters appear in the sentence bar; confidence updates live
5. Use `del` / `space` signs while signing to edit the sentence

## 🔌 API Reference

| Endpoint | Method | Description | Response |
|----------|--------|-------------|----------|
| `/` | GET | Serves the built React app | HTML |
| `/video_feed` | GET | Live annotated MJPEG stream | `multipart/x-mixed-replace` |
| `/get_prediction` | GET | Current prediction state | `{sentence, accuracy, current_action, current_confidence}` |
| `/api/reset` | POST | Clears sentence & state | `{status, message}` |
| `/api/actions` | GET | Supported gesture labels | `["A", "B", ...]` |

```javascript
// Poll current state (the frontend does this every 500 ms)
const res = await fetch('/get_prediction');
const { sentence, accuracy, current_action } = await res.json();

// Reset detection state
await fetch('/api/reset', { method: 'POST' });
```

## 🧠 Model Details

### Architecture (28×28 grayscale input)

```
Layer (type)              | Output Shape     | Notes
--------------------------|------------------|-----------------------------
Conv2D ×2 (64 filters)    | 28×28 → 14×14    | ReLU, same padding, BatchNorm
MaxPooling2D + Dropout    | 14×14            | dropout 0.25
Conv2D ×2 (128 filters)   | 14×14 → 7×7      | ReLU, same padding, BatchNorm
MaxPooling2D + Dropout    | 7×7              | dropout 0.25
Flatten → Dense(64)       | 64               | BatchNorm, dropout 0.5
Dense(32)                 | 32               | ReLU
Dense(num_classes)        | 29               | Softmax
```

### Training Configuration

| Parameter | Value |
|-----------|-------|
| Optimizer | Adam (lr = 1e-3) |
| Loss | Categorical crossentropy |
| Epochs | 30 (EarlyStopping patience = 5) |
| Batch size | 64 |
| Validation split | 10% (stratified) |
| LR schedule | ReduceLROnPlateau (factor 0.5, patience 3) |
| Input size | 28×28×1 grayscale, normalized to [0, 1] |
| Logs | TensorBoard → `Logs/cnn` |

> 🖥️ **Training strictly requires a GPU** — `trainmodel_cnn.py` exits if none is detected. On Windows use TensorFlow 2.10 + CUDA 11.2 + cuDNN 8.1, or WSL2.

### Retraining

Place the ASL alphabet dataset at `static/archive (3)/asl_alphabet_train/asl_alphabet_train` (one subfolder per class), then:

```bash
python trainmodel_cnn.py
```

This regenerates `model_cnn.h5`, `model_cnn.json`, and `model_cnn_labels.json`. Monitor progress with:

```bash
tensorboard --logdir=Logs
```

## ⚙️ Tunable Settings

| Setting | Location | Default | Effect |
|---------|----------|---------|--------|
| Confidence threshold | `app.py` → `threshold` | `0.6` | Minimum softmax score to accept a frame |
| Stability window | `app.py` → `predictions[-10:]` | `10` frames | Consecutive matching predictions before commit |
| Sentence length | `app.py` | `5` chars | Rolling sentence buffer |
| JPEG quality | `app.py` | `80` | Stream quality vs bandwidth |
| Mirror display | `app.py` → `MIRROR_DISPLAY` | `False` | Flip video horizontally |
| Detection confidence | `function.py` usage in `app.py` | `0.5` | MediaPipe sensitivity |
| Model complexity | `app.py` | `0` | `0` = fastest, `1` = more accurate |

## 🐛 Troubleshooting

<details>
<summary><b>Camera could not be opened</b></summary>

Close other apps using the webcam, check OS camera permissions, or try a different USB port.
</details>

<details>
<summary><b>Stuck on "Waiting..." (no hand detected)</b></summary>

Keep your hand fully inside the orange ROI box, improve lighting, and reduce background clutter.
</details>

<details>
<summary><b>TensorFlow import errors</b></summary>

Pin the supported stack:

```bash
pip uninstall tensorflow numpy -y
pip install tensorflow==2.10.0 numpy
```
</details>

<details>
<summary><b>Port 5000 already in use</b></summary>

```powershell
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

Or change the port in `app.py`: `serve(app, host='127.0.0.1', port=5001, threads=6)`
</details>

<details>
<summary><b>Frontend shows stale content after rebuild</b></summary>

Rebuild and hard-refresh — the backend already disables static caching:

```bash
cd frontend && npm run build
```
</details>

<details>
<summary><b>Slow performance</b></summary>

Lower JPEG quality (`cv2.IMWRITE_JPEG_QUALITY, 60`), keep `model_complexity=0`, or reduce the polling interval in `frontend/src/components/Prediction.jsx`.
</details>

## 🧪 Quick Sanity Checks

```bash
# Imports
python -c "import tensorflow, mediapipe, cv2, flask; print('All imports OK')"

# Model loads
python -c "from tensorflow.keras.models import load_model; load_model('model_cnn.h5', compile=False); print('Model OK')"

# Label map matches model output
python -c "import json; m=json.load(open('model_cnn_labels.json')); print(len(m), 'classes')"
```

## 🔒 Privacy & Security

- All inference runs locally — **no video ever leaves your machine**
- Server binds to `127.0.0.1` only; nothing is exposed to the network
- No telemetry, storage, or transmission of personal data

## 🗺️ Roadmap

- [x] Single-hand static gesture recognition
- [x] Full A–Z alphabet with control tokens
- [x] Web interface with live feedback
- [x] Sentence construction with stability filtering
- [ ] Dynamic/motion gesture recognition (two-handed signs)
- [ ] Word-level recognition & auto-spacing
- [ ] Text-to-speech voice feedback
- [ ] Mobile-friendly layout & PWA support
- [ ] ONNX / TensorFlow Lite export for edge deployment

## 🙏 Acknowledgments

- [Google MediaPipe](https://developers.google.com/mediapipe) — hand tracking
- [TensorFlow / Keras](https://www.tensorflow.org/) — deep learning framework
- [ASL Alphabet Dataset](https://www.kaggle.com/datasets/grassknoted/asl-alphabet) — training data
- [React](https://react.dev/) & [Vite](https://vitejs.dev/) — frontend tooling

---

**Version:** 2.0.0 (CNN architecture) · **Status:** Production Ready · **Last Updated:** August 2026

*Final year academic project — please cite appropriately if used in research.*
