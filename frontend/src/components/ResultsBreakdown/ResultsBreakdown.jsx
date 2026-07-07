import { useState, useEffect } from "react";
import "./ResultsBreakdown.css";

const PHASE_LABELS = {
  LOADING: "Loading",
  SET_POINT: "Set Point",
  RELEASE: "Release",
};

function ResultsBreakdown({ snapshots = {}, feedback = {} }) {
  const phases = Object.keys(snapshots);

  const [activePhase, setActivePhase] = useState(null);

  // ✅ ensure active tab always exists after data loads
  useEffect(() => {
    if (phases.length && !activePhase) {
      setActivePhase(phases[0]);
    }
  }, [phases, activePhase]);

  if (!phases.length || !activePhase) return null;

  const getStatusClass = (status) => {
    switch (status) {
      case "good":
        return "good";
      case "uncertain":
        return "uncertain";
      default:
        return "bad";
    }
  };

  return (
    <div>
      {/* TAB BUTTONS */}
      <div className="tabs">
        {phases.map((phase) => (
          <button
            key={phase}
            onClick={() => setActivePhase(phase)}
            className={`tab-button ${
              activePhase === phase ? "active-tab" : ""
            }`}
          >
            {PHASE_LABELS[phase] || phase}
          </button>
        ))}
      </div>

      {/* ACTIVE TAB CONTENT */}
      <div className="tab-content">
        <h3>{PHASE_LABELS[activePhase] || activePhase}</h3>

        <img
          src={`http://localhost:8000${snapshots[activePhase]}`}
          alt={activePhase}
          style={{ width: 320, borderRadius: 8 }}
        />

        <h4>Feedback</h4>

        {feedback?.[activePhase] ? (
          <div className="feedback-card">
            {Object.entries(feedback[activePhase]).map(([joint, info]) => (
              <div
                key={joint}
                className={`feedback-item ${getStatusClass(info.status)}`}
              >
                <strong>
                  {joint
                    .replace(/_/g, " ")
                    .replace(/\b\w/g, (c) => c.toUpperCase())}
                </strong>

                {typeof info.angle === "number" && (
                  <>
                    : {info.angle.toFixed(1)}°
                    {info.ideal && (
                      <span className="target-range">
                        {" "}
                        (Target: {info.ideal[0]}°–{info.ideal[1]}°)
                      </span>
                    )}
                  </>
                )}

                <br />
                <span>{info.message}</span>
              </div>
            ))}
          </div>
        ) : (
          <p>No feedback available.</p>
        )}
      </div>
    </div>
  );
}

export default ResultsBreakdown;