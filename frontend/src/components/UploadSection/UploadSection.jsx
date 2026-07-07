import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./UploadSection.css";

function UploadSection() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  const navigate = useNavigate();

  const upload = async () => {
    if (!file) return;

    setUploading(true);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch("http://localhost:8000/upload-and-analyze", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        throw new Error("Upload failed");
      }

      const data = await res.json();
      const jobId = data.job_id;

      navigate(`/results/${jobId}`);
    } catch (err) {
      console.error(err);
      alert("Upload failed");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="upload-button">
      <input
        type="file"
        accept="video/*"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button onClick={upload} disabled={!file || uploading}>
        {uploading ? "Uploading..." : "Upload Video"}
      </button>
    </div>
  );
}

export default UploadSection;