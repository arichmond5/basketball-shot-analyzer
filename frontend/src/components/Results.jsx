import "./results.css"

function Results() {
  return (
    <section className="results" id="results">
      <h2>Your Shot Analysis</h2>

      <div className="result-card">
        <h3>Form Score: 78/100</h3>
      </div>

      <div className="result-card">
        <h3>Breakdown</h3>
        <ul>
          <li>Elbow alignment: good</li>
          <li>Knee bend: inconsistent</li>
          <li>Release timing: needs improvement</li>
        </ul>
      </div>

      <div className="result-card">
        <h3>Suggestion</h3>
        <p>Focus on keeping your elbow under the ball during release.</p>
      </div>
    </section>
  );
}

export default Results;