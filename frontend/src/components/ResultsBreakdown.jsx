import { useState } from "react";
import "./ResultsBreakdown.css";

const PHASE_LABELS = {
  LOADING: "Dip",
  SET_POINT: "Set Point",
  FOLLOW_THROUGH: "Follow Through",
};

function ResultsBreakdown({ snapshots = {}, feedback = {} }) {
  const phases = Object.keys(snapshots);

  if (!phases.length) return null;

  const [activePhase, setActivePhase] = useState(phases[0]);

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
          src={snapshots[activePhase]}
          alt={activePhase}
          style={{ width: 320, borderRadius: 8 }}
        />

        {feedback?.[activePhase] && (
          <div className="feedback-card">
            {Object.entries(feedback[activePhase]).map(([joint, info]) => (
              <div
                key={joint}
                className={`feedback-item ${
                  info?.status === "good" ? "good" : "bad"
                }`}
              >
                <strong>{joint}</strong>:{" "}
                {info?.angle?.toFixed?.(1) ?? "N/A"}° —{" "}
                {info?.message ?? ""}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default ResultsBreakdown;