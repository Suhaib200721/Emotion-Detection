import cv2
from deepface import DeepFace


def detect_emotion(frame):
    result = DeepFace.analyze(
        frame,
        actions=["emotion"],
        enforce_detection=False
    )

    return result[0]["dominant_emotion"]


def run_webcam():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Camera not found")
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Camera not found")
            break

        try:
            emotion = detect_emotion(frame)

            cv2.putText(
                frame,
                "Emotion: " + emotion,
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

        except Exception:
            print("Detection error")

        cv2.imshow("Emotion Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_webcam()