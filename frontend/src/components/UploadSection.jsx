import { useState } from "react";
import "./UploadSection.css";

function UploadSection() {
  const [video, setVideo] = useState(null);

  function handleVideoChange(event) {
    setVideo(event.target.files[0]);
  }

  return (
    <div className="upload-section">
      <label className="uploadButton">
        Upload Video
        <input
          type="file"
          accept="video/*"
          onChange={handleVideoChange}
          hidden
        />
      </label>
    </div>
  );
}

export default UploadSection;