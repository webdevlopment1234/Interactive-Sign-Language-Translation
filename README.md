# Real-Time Hand Gesture Recognition System

A complete deep learning-based sign language recognition system that translates hand gestures into text in real-time using MediaPipe for hand landmark detection and LSTM neural networks for gesture classification.

## 🌟 Features

- **Real-time Gesture Recognition**: Live webcam processing with instant gesture-to-text translation
- **MediaPipe Integration**: Google's MediaPipe Hands for accurate 21-point hand landmark detection
- **LSTM Neural Network**: Sequential model architecture for temporal gesture recognition
- **Web-based Interface**: Modern React frontend with Flask backend API
- **Sentence Construction**: Builds complete sentences from consecutive gesture predictions
- **Confidence Scoring**: Real-time accuracy percentage display for each prediction
- **Visual Feedback**: On-screen landmarks, ROI box, and prediction overlay
- **Responsive Design**: Works on various screen sizes with gradient UI design

## 📋 System Architecture

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────────┐
│   Webcam Input  │ ──▶ │  MediaPipe   │ ──▶ │   Feature   │ ──▶ │    LSTM      │
│                 │     │   Hands      │     │  Extraction │     │   Model      │
└─────────────────┘     └──────────────┘     └─────────────┘     └──────────────┘
                                                                        │
                                                                        ▼
┌─────────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────────┐
│  Display Result │ ◀── │   Sentence   │ ◀── │  Prediction │ ◀── │  Softmax     │
│                 │     │  Builder     │     │  Filtering  │     │  Output      │
└─────────────────┘     └──────────────┘     └─────────────┘     └──────────────┘
```

## 🎯 Supported Gestures

The system recognizes **13 different hand signs**:
- **Letters**: A, B, C
- **Numbers**: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9

## 🛠️ Technology Stack

### Backend
- **Python 3.8+**
- **TensorFlow 2.10.0** - Deep learning framework
- **Keras 2.10.0** - Neural network API
- **MediaPipe 0.10.32** - Hand landmark detection
- **OpenCV** - Computer vision operations
- **Flask** - Web server framework
- **Waitress** - Production WSGI server
- **NumPy** - Numerical computations
- **scikit-learn** - Machine learning utilities

### Frontend
- **React 19.2.0** - UI framework
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Lucide React** - Icon library

## 📁 Project Structure

```
4-yearfinalreview/
├── app.py                      # Flask backend server with video streaming
├── function.py                 # MediaPipe processing and feature extraction
├── data.py                     # Data collection script for training data
├── collectdata.py              # Webcam capture tool for dataset creation
├── trainmodel.py               # LSTM model training script
├── model.json                  # Saved model architecture
├── model.h5                    # Trained model weights
├── frontend/                   # React frontend application
│   ├── src/
│   │   ├── App.jsx            # Main React component
│   │   ├── main.jsx           # Application entry point
│   │   ├── index.css          # Global styles
│   │   └── components/        # Reusable UI components
│   │       ├── Navbar.jsx
│   │       ├── Hero.jsx
│   │       ├── Prediction.jsx  # Real-time prediction interface
│   │       ├── Learning.jsx
│   │       └── Quiz.jsx
│   ├── public/
│   ├── dist/                   # Production build output
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── Image/                      # Raw image dataset (collected via collectdata.py)
│   ├── A/, B/, C/             # Letter gesture folders
│   └── 0/, 1/, ..., 9/        # Number gesture folders
├── MP_Data/                    # Processed MediaPipe landmark data
│   └── [A-Z, 0-9]/            # NPY files with keypoints
├── Logs/                       # TensorBoard training logs
└── static/                     # Static assets
```

## 🚀 Installation & Setup

### Prerequisites

- **Python 3.8 or higher**
- **Node.js 16+** (for frontend development)
- **Webcam** with camera access
- **Modern web browser** (Chrome, Firefox, Edge recommended)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd 4-yearfinalreview
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv_new

# Activate virtual environment
# Windows:
venv_new\Scripts\activate
# Linux/Mac:
source venv_new/bin/activate
```

### Step 3: Install Python Dependencies

```bash
pip install tensorflow==2.10.0
pip install keras==2.10.0
pip install mediapipe==0.10.32
pip install opencv-python
pip install opencv-contrib-python
pip install flask
pip install waitress
pip install numpy==1.24.3
pip install scikit-learn
pip install matplotlib
```

### Step 4: Install Frontend Dependencies

```bash
cd frontend
npm install
```

### Step 5: Verify Model Files

Ensure you have the trained model files in the root directory:
- `model.json` - Model architecture
- `model.h5` - Model weights

If not present, run the training script first (see Training section).

## 🎮 Usage

### Starting the Application

#### Option 1: Run Backend Only (Development)

```bash
# From project root directory
python app.py
```

The server will start at: **http://127.0.0.1:5000**

#### Option 2: Run Frontend Development Server

```bash
# Terminal 1 - Start backend
python app.py

# Terminal 2 - Start frontend (in separate terminal)
cd frontend
npm run dev
```

Frontend will be available at: **http://localhost:5173**

#### Option 3: Production Mode

```bash
# Build frontend first
cd frontend
npm run build

# Then run backend (serves static files)
cd ..
python app.py
```

### Using the Application

1. **Access the Web Interface**: Open your browser and navigate to `http://127.0.0.1:5000`

2. **Navigate to Prediction Section**: Click on "Prediction" or "Start Detection"

3. **Grant Camera Permissions**: Allow browser to access your webcam when prompted

4. **Position Your Hand**: 
   - Place your right hand in the blue rectangular detection zone
   - Keep hand steady within the ROI (Region of Interest) box
   - Ensure good lighting for optimal detection

5. **Perform Gestures**: 
   - Hold each gesture for 1-2 seconds
   - The system requires 30 consecutive frames (≈1 second) for prediction
   - Watch the confidence score update in real-time

6. **View Results**: 
   - Current gesture appears with confidence percentage
   - Detected sentence builds at the top of the video feed
   - Results update automatically as new gestures are recognized

### Expected Output Format

When a gesture is detected, you'll see:
```
Hand Gesture: A
Accuracy: 95.3%
Background: Dark/Indoor
Detected Sentence: A B C 1 2 3
```

## 🔧 API Endpoints

The Flask backend exposes several REST API endpoints:

| Endpoint | Method | Description | Response |
|----------|--------|-------------|----------|
| `/` | GET | Serve main HTML page | HTML content |
| `/video_feed` | GET | Stream processed video with landmarks | Multipart JPEG stream |
| `/get_prediction` | GET | Get current prediction results | JSON: `{sentence, accuracy, current_action, current_confidence}` |
| `/api/reset` | POST | Reset detection state | JSON: `{status, message}` |
| `/api/actions` | GET | List all supported gestures | JSON: Array of action names |
| `/static/*` | GET | Serve static frontend assets | Static files |

### Example API Usage

```javascript
// Get current prediction
fetch('/get_prediction')
  .then(res => res.json())
  .then(data => {
    console.log('Current gesture:', data.current_action);
    console.log('Confidence:', data.current_confidence);
    console.log('Sentence:', data.sentence);
  });

// Reset detection state
fetch('/api/reset', { method: 'POST' })
  .then(res => res.json())
  .then(data => console.log('Reset complete'));

// Get list of actions
fetch('/api/actions')
  .then(res => res.json())
  .then(actions => console.log('Supported gestures:', actions));
```

## 🧠 Model Architecture

### LSTM Network Structure

```
Layer Type          | Units | Activation    | Input Shape
--------------------|-------|---------------|------------------
LSTM                | 64    | ReLU          | (30, 63)
LSTM                | 128   | ReLU          | (30, 64)
LSTM                | 64    | ReLU          | (30, 128)
Dense               | 64    | ReLU          | (64,)
Dense               | 32    | ReLU          | (64,)
Dense (Output)      | 13    | Softmax       | (32,)
```

### Model Configuration

- **Optimizer**: Adam
- **Loss Function**: Categorical Crossentropy
- **Metrics**: Categorical Accuracy
- **Training Epochs**: 200
- **Batch Size**: Auto (default)
- **Sequence Length**: 30 frames
- **Feature Vector**: 63 values (21 landmarks × 3 coordinates)

### Training Parameters

```python
model.compile(
    optimizer='Adam',
    loss='categorical_crossentropy',
    metrics=['categorical_accuracy']
)

model.fit(
    X_train, y_train,
    epochs=200,
    validation_data=(X_test, y_test),
    callbacks=[TensorBoard(log_dir='Logs')]
)
```

## 📊 Data Collection & Training

### Collecting Training Data

1. **Run Data Collection Script**:

```bash
python collectdata.py
```

2. **Capture Images**:
   - Press keys 'a', 'b', 'c' for letters
   - Press keys '0'-'9' for numbers
   - Each press saves an image to the corresponding folder
   - Collect 100+ images per gesture for best results

3. **Process Images to Landmarks**:

```bash
python data.py
```

This script:
- Loads each captured image
- Runs MediaPipe hand detection
- Extracts 21 hand landmarks (x, y, z coordinates)
- Saves normalized keypoints as `.npy` files

### Training the Model

```bash
python trainmodel.py
```

The training script will:
1. Load all processed landmark data from `MP_Data/`
2. Create sequences of 30 frames
3. Split data into training (95%) and testing (5%) sets
4. Train the LSTM model for 200 epochs
5. Save the trained model to `model.json` and `model.h5`
6. Log training metrics to TensorBoard in `Logs/`

### Monitoring Training

```bash
# Launch TensorBoard to visualize training progress
tensorboard --logdir=Logs
```

Then open: `http://localhost:6006`

## ⚙️ Configuration

### Detection Settings (in `app.py`)

```python
threshold = 0.6  # Confidence threshold for gesture acceptance
MIRROR_DISPLAY = False  # Mirror the video display (not detection)
```

### MediaPipe Parameters (in `function.py`)

```python
mp_hands.Hands(
    model_complexity=0,           # 0=fastest, 1=accurate
    min_detection_confidence=0.5, # Minimum detection confidence
    min_tracking_confidence=0.5   # Minimum tracking confidence
)
```

### Model Hyperparameters

Adjust in `trainmodel.py`:
- Number of LSTM layers and units
- Dense layer configuration
- Learning rate (via optimizer)
- Dropout for regularization

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 1. Camera Not Opening

**Error**: `CRITICAL: Camera could not be opened`

**Solutions**:
- Check if another application is using the camera
- Verify camera permissions in browser settings
- Try a different USB port for external webcams
- Update camera drivers

#### 2. No Hand Detection

**Symptoms**: Landmarks not appearing, always shows "Waiting..."

**Solutions**:
- Ensure hand is fully visible in the ROI box
- Improve lighting conditions
- Move hand closer to camera
- Reduce background clutter
- Check if MediaPipe model file exists

#### 3. Low Accuracy Predictions

**Symptoms**: Confidence below 60%, inconsistent results

**Solutions**:
- Retrain model with more diverse dataset
- Ensure consistent hand positioning during training
- Increase sequence length for temporal context
- Adjust confidence threshold in `app.py`

#### 4. TensorFlow Import Errors

**Error**: `AttributeError: module 'tensorflow' has no attribute 'config'`

**Solution**: Use compatible versions:
```bash
pip uninstall tensorflow
pip install tensorflow==2.10.0
pip install numpy==1.24.3
```

#### 5. MediaPipe API Errors

**Error**: `AttributeError: module 'mediapipe' has no attribute 'solutions'`

**Solution**: MediaPipe 0.10.32 uses new API structure. Ensure `function.py` imports correctly:
```python
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
```

#### 6. Flask Server Won't Start

**Error**: Port 5000 already in use

**Solution**:
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Or change port in app.py
serve(app, host='127.0.0.1', port=5001, threads=6)
```

#### 7. Frontend Build Errors

**Error**: Module not found or build fails

**Solution**:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Performance Optimization

#### For Slower Systems

1. Reduce model complexity in `function.py`:
```python
mp_hands.Hands(model_complexity=0, ...)
```

2. Lower video quality in `app.py`:
```python
ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 60])
```

3. Reduce prediction frequency in frontend

#### For Better Accuracy

1. Increase training data diversity
2. Train for more epochs (300+)
3. Use higher model complexity
4. Implement data augmentation
5. Add more gesture classes gradually

## 🧪 Testing

### Quick Test

After installation, verify everything works:

```bash
# Test Python imports
python -c "import tensorflow as tf; import mediapipe as mp; import cv2; print('All imports successful!')"

# Test model loading
python -c "from keras.models import model_from_json; m = model_from_json(open('model.json').read()); m.load_weights('model.h5'); print('Model loaded successfully!')"

# Test MediaPipe
python -c "from function import *; print('MediaPipe functions loaded!')"
```

### Unit Testing

Create test scripts to verify:
- Camera accessibility
- MediaPipe landmark detection
- Model prediction functionality
- API endpoint responses

## 📈 Performance Metrics

### Typical Performance

- **Detection Speed**: ~30 FPS on modern hardware
- **Prediction Latency**: <100ms per frame
- **Model Size**: ~2.3 MB (compressed)
- **Accuracy**: 95-98% on test set (varies by gesture)

### Benchmarking

Run performance tests:
```python
import time
start = time.time()
# Run prediction
end = time.time()
print(f"Inference time: {(end-start)*1000:.2f}ms")
```

## 🔒 Security Considerations

- Camera access requires user permission
- All processing happens locally (no cloud dependency)
- No personal data is stored or transmitted
- Flask server only accessible on localhost by default

## 🤝 Contributing

To contribute improvements:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Areas for Improvement

- Add support for continuous sign language (full sentences)
- Implement multi-hand detection
- Add more gesture classes (full alphabet)
- Optimize for mobile deployment
- Create desktop application version
- Add user authentication and profiles
- Implement model retraining from collected data

## 📄 License

This project is created as a final year academic project. Please cite appropriately if used in research or publications.

## 👥 Authors

**Final Year Project** - Hand Gesture Recognition System

## 🙏 Acknowledgments

- **Google MediaPipe** - Hand landmark detection framework
- **TensorFlow Team** - Deep learning framework
- **React Team** - Frontend library
- **Academic Advisors** - Guidance and support

## 📞 Support

For issues or questions:

1. Check this README thoroughly
2. Review the Troubleshooting section
3. Check TensorBoard logs for training issues
4. Examine Flask console output for runtime errors
5. Use browser DevTools for frontend debugging

## 🗺️ Roadmap

### Phase 1: Core Features ✅
- [x] Single hand gesture recognition
- [x] Real-time webcam integration
- [x] Web-based interface
- [x] Sentence construction

### Phase 2: Enhanced Features (Future)
- [ ] Continuous sign language translation
- [ ] Multi-hand detection
- [ ] Voice feedback
- [ ] Mobile app version
- [ ] User customization interface
- [ ] Cloud model serving
- [ ] Historical data tracking

### Phase 3: Advanced Capabilities (Future)
- [ ] Full ASL alphabet support
- [ ] Dynamic gesture recognition
- [ ] Two-way communication mode
- [ ] Multi-language support
- [ ] Accessibility features

## 📚 Additional Resources

- [MediaPipe Documentation](https://google.github.io/mediapipe/)
- [TensorFlow Tutorials](https://www.tensorflow.org/tutorials)
- [Keras API Reference](https://keras.io/api/)
- [OpenCV Documentation](https://docs.opencv.org/)
- [React Documentation](https://react.dev/)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

**Last Updated**: March 2026  
**Version**: 1.0.0  
**Status**: Production Ready
