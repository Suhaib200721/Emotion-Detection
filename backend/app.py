import cv2
import numpy as np
from flask import Flask, jsonify, request
from flask_cors import CORS

from emotion_detection import detect_emotion

app = Flask(__name__)
CORS(app)


@app.get("/api/health")
def health_check():
    return jsonify({"status": "ok"})


@app.post("/api/detect-emotion")
def detect_emotion_route():
    uploaded_file = request.files.get("image")

    if uploaded_file is None or not uploaded_file.filename:
        return jsonify({"error": "Please upload an image."}), 400

    image_bytes = uploaded_file.read()
    if not image_bytes:
        return jsonify({"error": "The uploaded image is empty."}), 400

    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        return jsonify({"error": "The uploaded file is not a valid image."}), 400

    try:
        emotion = detect_emotion(image)
    except Exception:
        return jsonify({"error": "Emotion detection failed. Try another image."}), 500

    return jsonify({"emotion": emotion})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
