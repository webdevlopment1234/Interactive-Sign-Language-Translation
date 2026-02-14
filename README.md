# Hand Gesture Recognition Frontend

A modern web-based frontend for the hand gesture recognition system using React and Flask.

## Features

- Real-time webcam integration
- Live gesture detection and recognition
- Beautiful responsive UI with gradient design
- Real-time results display in the required format:
  - Hand Gesture:
  - Accuracy:
  - Background:
  - Detected Sentence:
- Model status monitoring
- Error handling and user feedback

## Prerequisites

- Node.js (v16 or higher)
- Python 3.8+
- The trained model files (model.json and model.h5) from your existing system

## Setup Instructions

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Make sure your model files are in the root directory
# (model.json and model.h5 should be in the parent directory)

# Start the Flask backend
python app.py
```

The backend will run on `http://localhost:5000`

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (if not already done)
npm install

# Start the development server
npm run dev
```

The frontend will run on `http://localhost:5173`

## Usage

1. Start both the backend and frontend servers
2. Open your browser and go to `http://localhost:5173`
3. Click "开始检测" (Start Detection) to begin
4. Allow camera permissions when prompted
5. Place your hand in the detection area (blue box)
6. View real-time gesture recognition results

## API Endpoints

- `GET /api/status` - Check model status
- `POST /api/detect` - Process image and detect gestures
- `POST /api/reset` - Reset detection state

## File Structure

```
4-yearfinalreview/
├── backend/
│   ├── app.py              # Flask backend server
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main React component
│   │   ├── App.css         # Styling
│   │   └── index.css       # Base styles
│   └── package.json        # Frontend dependencies
├── model.json              # Trained model architecture
├── model.h5                # Trained model weights
└── function.py             # Helper functions
```

## Troubleshooting

### Common Issues:

1. **"Model Not Loaded"**: Make sure your model.json and model.h5 files are in the root directory
2. **Camera not working**: Check browser permissions and try a different browser
3. **Connection errors**: Ensure the backend is running on port 5000
4. **Detection not working**: Make sure sufficient lighting and clear hand visibility

### Browser Compatibility:

- Chrome (recommended)
- Firefox
- Edge
- Safari (limited support)

## Development

To modify the frontend:
- Edit `src/App.jsx` for functionality changes
- Edit `src/App.css` for styling changes
- The development server supports hot reloading

To modify the backend:
- Edit `backend/app.py` for API changes
- Restart the Flask server after changes

## Deployment

For production deployment:
1. Build the React app: `npm run build`
2. Update Flask app.py to serve static files from the dist folder
3. Deploy both backend and frontend to your preferred hosting platform