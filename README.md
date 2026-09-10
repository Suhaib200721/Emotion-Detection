# Emotion Detection

A simple web application that uses a React frontend and a Flask backend to detect the dominant emotion in a camera capture or uploaded image.

## Features

- Real-time camera capture
- Image upload
- Emotion detection
- Dominant emotion result

## Technologies

- React.js
- Vite
- JavaScript
- Python
- Flask
- OpenCV
- DeepFace

## How to Run

Backend:

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal. Allow camera access to use the camera capture, or choose a JPG, JPEG, or PNG image to upload.

The original desktop OpenCV webcam mode is still available with:

```bash
python emotion_detection.py
```
