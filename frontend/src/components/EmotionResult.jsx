function EmotionResult({ emotion, loading }) {
  return (
    <section className="result-card" aria-live="polite">
      <p className="result-label">Detected Emotion</p>
      {loading ? (
        <p className="result-value muted-result">Analyzing...</p>
      ) : emotion ? (
        <>
          <p className="result-value">{emotion}</p>
          <p className="success-message">Emotion detected successfully.</p>
        </>
      ) : (
        <p className="result-value muted-result">No result yet</p>
      )}
    </section>
  );
}

export default EmotionResult;
