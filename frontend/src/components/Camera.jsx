import { useEffect, useRef, useState } from "react";

function Camera({ onCapture, disabled }) {
  const videoRef = useRef(null);
  const streamRef = useRef(null);
  const [cameraMessage, setCameraMessage] = useState("");
  const [cameraStarted, setCameraStarted] = useState(false);

  useEffect(() => {
    return () => {
      streamRef.current?.getTracks().forEach((track) => track.stop());
    };
  }, []);

  async function startCamera() {
    setCameraMessage("");

    if (!navigator.mediaDevices?.getUserMedia) {
      setCameraMessage("Camera access is not available in this browser.");
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      streamRef.current = stream;
      videoRef.current.srcObject = stream;
      await videoRef.current.play();
      setCameraStarted(true);
    } catch {
      setCameraMessage("Camera permission was denied or the camera is unavailable.");
    }
  }

  function captureFrame() {
    const video = videoRef.current;
    if (!video?.videoWidth) {
      setCameraMessage("Start the camera before capturing an image.");
      return;
    }

    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext("2d").drawImage(video, 0, 0);
    canvas.toBlob((blob) => {
      if (blob) onCapture(blob);
    }, "image/jpeg");
  }

  return (
    <section className="panel">
      <h2>Camera</h2>
      <div className="camera-frame">
        <video
          ref={videoRef}
          className={`camera-preview ${cameraStarted ? "" : "hidden"}`}
          autoPlay
          muted
          playsInline
        />
        {!cameraStarted && (
          <p className="empty-preview">Your camera preview will appear here.</p>
        )}
      </div>
      <div className="button-row">
        <button className="button primary-button" onClick={startCamera} disabled={cameraStarted}>
          {cameraStarted ? "Camera Started" : "Start Camera"}
        </button>
        <button className="button secondary-button" onClick={captureFrame} disabled={disabled || !cameraStarted}>
          Capture
        </button>
      </div>
      {cameraMessage && <p className="inline-error">{cameraMessage}</p>}
    </section>
  );
}

export default Camera;
