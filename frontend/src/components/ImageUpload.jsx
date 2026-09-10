function ImageUpload({ onUpload, disabled }) {
  function handleChange(event) {
    const file = event.target.files?.[0];
    if (file) onUpload(file);
    event.target.value = "";
  }

  return (
    <section className="panel upload-panel">
      <h2>Upload an image</h2>
      <p className="helper-text">Choose a JPG, JPEG, or PNG image.</p>
      <label className={`upload-control ${disabled ? "disabled" : ""}`}>
        <span>Upload Image</span>
        <input type="file" accept="image/jpeg,image/png" onChange={handleChange} disabled={disabled} />
      </label>
    </section>
  );
}

export default ImageUpload;
