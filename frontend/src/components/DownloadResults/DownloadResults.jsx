import "./DownloadResults.css";

const API_URL = import.meta.env.VITE_API_URL;

function DownloadResults({ jobId }) {
  return (
    <div className="button-container">
      <a
        className="downloadButton"
        href={`${API_URL}/download/${jobId}`}
      >
        <span className="downloadIcon">⬇</span>
        Download Results
      </a>
    </div>
  );
}

export default DownloadResults;
