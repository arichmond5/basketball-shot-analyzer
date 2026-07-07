import "./DownloadResults.css";

function DownloadResults({ jobId }) {
  return (
    <div className="button-container">
      <a
        className="downloadButton"
        href={`http://localhost:8000/download/${jobId}`}
      >
        <span className="downloadIcon">⬇</span>
        Download Results
      </a>
    </div>
  );
}

export default DownloadResults;
