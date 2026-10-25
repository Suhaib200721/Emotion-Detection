"""Real-time facial emotion detection using OpenCV and DeepFace."""

from __future__ import annotations

import sys
import time
from typing import Any


WINDOW_NAME = "Emotion Detection System"
ANALYSIS_INTERVAL_SECONDS = 1.0
CAMERA_INDEX = 0
EMOTION_LABELS = {
    "angry": "Angry",
    "disgust": "Disgust",
    "fear": "Fear",
    "happy": "Happy",
    "sad": "Sad",
    "surprise": "Surprise",
    "neutral": "Neutral",
}


def _cleanup(camera: Any, cv2: Any) -> None:
    cleanup_errors: list[Exception] = []
    for cleanup_action in (camera.release, cv2.destroyAllWindows):
        try:
            cleanup_action()
        except Exception as exc:
            cleanup_errors.append(exc)

    if cleanup_errors:
        if sys.exc_info()[0] is not None:
            for error in cleanup_errors:
                print(f"OpenCV cleanup warning: {error}", file=sys.stderr)
        else:
            raise cleanup_errors[0]


def main() -> int:
    try:
        import cv2
        from deepface import DeepFace
        import numpy as np
    except (ImportError, OSError) as exc:
        print(
            "A required package could not be loaded. Activate the project "
            "virtual environment and run: python -m pip install -r requirements.txt",
            file=sys.stderr,
        )
        print(f"Import details: {exc}", file=sys.stderr)
        return 1

    camera = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)
    if not camera.isOpened():
        _cleanup(camera, cv2)
        print(
            "Could not access the webcam. Check that it is connected, close "
            "other apps using it, and allow camera access in Windows Settings.",
            file=sys.stderr,
        )
        return 1

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    if face_cascade.empty():
        _cleanup(camera, cv2)
        print("OpenCV could not load its frontal-face detector.", file=sys.stderr)
        return 1

    cached_faces: list[dict[str, Any]] = []
    next_analysis_at = 0.0
    analysis_message = ""

    print("Emotion detection is running. Press Q or Esc to quit.")
    try:
        while True:
            success, frame = camera.read()
            if not success or frame is None:
                print(
                    "The webcam stopped providing frames. Check the camera "
                    "connection and try again.",
                    file=sys.stderr,
                )
                return 1

            frame = np.asarray(frame)
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            detected_faces = face_cascade.detectMultiScale(
                gray_frame,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(40, 40),
            )
            now = time.monotonic()

            if len(detected_faces) == 0:
                cached_faces = []
                analysis_message = ""
            elif now >= next_analysis_at:
                next_analysis_at = now + ANALYSIS_INTERVAL_SECONDS
                try:
                    results = DeepFace.analyze(
                        img_path=frame,
                        actions=["emotion"],
                        detector_backend="opencv",
                        enforce_detection=True,
                        silent=True,
                    )
                except ValueError as exc:
                    # OpenCV's lightweight detector can find a face that the
                    # DeepFace detector cannot reliably analyze.
                    cached_faces = []
                    analysis_message = "Face detected; analysis unavailable"
                    print(f"Could not analyze the detected face: {exc}", file=sys.stderr)
                else:
                    if isinstance(results, dict):
                        results = [results]
                    cached_faces = [
                        result
                        for result in results
                        if isinstance(result, dict)
                        and isinstance(result.get("region"), dict)
                        and isinstance(result.get("emotion"), dict)
                        and result["emotion"]
                    ]
                    analysis_message = (
                        "" if cached_faces else "No face could be analyzed"
                    )

            if len(detected_faces) == 0:
                cv2.putText(
                    frame,
                    "No face detected",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 165, 255),
                    2,
                    cv2.LINE_AA,
                )
            elif analysis_message:
                cv2.putText(
                    frame,
                    analysis_message,
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    (0, 165, 255),
                    2,
                    cv2.LINE_AA,
                )

            for face in cached_faces:
                region = face["region"]
                x = max(0, int(region.get("x", 0)))
                y = max(0, int(region.get("y", 0)))
                width = max(0, int(region.get("w", 0)))
                height = max(0, int(region.get("h", 0)))
                if width == 0 or height == 0:
                    continue

                emotion_scores = face["emotion"]
                dominant_emotion = str(
                    face.get("dominant_emotion")
                    or max(emotion_scores, key=emotion_scores.get)
                ).lower()
                confidence = float(emotion_scores.get(dominant_emotion, 0.0))
                emotion_name = EMOTION_LABELS.get(
                    dominant_emotion, dominant_emotion.title()
                )
                label = f"{emotion_name}: {confidence:.1f}%"

                cv2.rectangle(
                    frame, (x, y), (x + width, y + height), (0, 255, 0), 2
                )
                label_y = max(y - 10, 25)
                cv2.putText(
                    frame,
                    label,
                    (x, label_y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2,
                    cv2.LINE_AA,
                )

            try:
                cv2.imshow(WINDOW_NAME, frame)
            except cv2.error as exc:
                if "function is not implemented" in str(exc).lower():
                    raise RuntimeError(
                        "This OpenCV installation has no GUI support. Remove "
                        "headless OpenCV packages and reinstall the project "
                        "requirements."
                    ) from exc
                raise
            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), 27):
                break
    finally:
        _cleanup(camera, cv2)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
