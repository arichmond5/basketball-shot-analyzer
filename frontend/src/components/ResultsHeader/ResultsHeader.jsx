import "./ResultsHeader.css";

function ResultsHeader({ url }) {
  const videoUrl = url
    ? `http://localhost:8000${url}`
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