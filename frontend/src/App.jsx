import { useState } from "react";
import Camera from "./components/Camera";
import EmotionResult from "./components/EmotionResult";
import ImageUpload from "./components/ImageUpload";

const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:5000";

function App() {
  const [emotion, setEmotion] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function detectEmotion(image) {
    setError("");
    setEmotion("");
    setLoading(true);

    const formData = new FormData();
    formData.append("image", image, image.name || "camera-capture.jpg");

    try {
      const response = await fetch(`${apiUrl}/api/detect-emotion`, {
        method: "POST",
        body: formData
      });
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Emotion detection failed.");
      }

      setEmotion(data.emotion);
    } catch (requestError) {
      setError(requestError.message || "The backend is unavailable. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app-shell">
      <header className="page-header">
        <p className="eyebrow">Computer vision project</p>
        <h1>Emotion Detection</h1>
        <p className="intro">Capture a face with your camera or upload an image to detect its dominant emotion.</p>
      </header>

      <div className="content-grid">
        <Camera onCapture={detectEmotion} disabled={loading} />
        <ImageUpload onUpload={detectEmotion} disabled={loading} />
      </div>

      {error && <p className="error-message">{error}</p>}
      <EmotionResult emotion={emotion} loading={loading} />
    </main>
  );
}

export default App;
