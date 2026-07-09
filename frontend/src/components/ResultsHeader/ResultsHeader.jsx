import "./ResultsHeader.css";

const API_URL = import.meta.env.VITE_API_URL;

function ResultsHeader({ url }) {
  const videoUrl = url
    ? `${API_URL}${url}`
    : null;

  return (
    <section className="results-header">
      <h1>Results</h1>

      {videoUrl && (
        <video
          className="analysis-video"
          src={videoUrl}
          controls
        />
      )}
    </section>
  );
}

export default ResultsHeader;