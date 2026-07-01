import "./ResultsHeader.css";

function ResultsHeader({ url }) {
  return (
    <section className="results-header">
      <h1 className="results-title">Results</h1>

      {url && (
        <video className="analysis-video" src={url} controls />
      )}
    </section>
  );
}

export default ResultsHeader;