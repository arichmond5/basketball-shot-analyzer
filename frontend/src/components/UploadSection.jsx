import { useState } from "react";
import { useNavigate } from "react-router-dom";

function UploadSection() {
  const [file, setFile] = useState(null);

  const navigate = useNavigate();

  const upload = () => {
    if (!file) return;

    navigate("/results", {
      state: { file },
    });
  };

  return (
    <div>
      <input
        type="file"
        accept="video/*"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button onClick={upload} disabled={!file}>
        Upload Video
      </button>
    </div>
  );
}

export default UploadSection;