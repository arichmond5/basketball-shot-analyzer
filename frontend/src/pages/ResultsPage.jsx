import { useLocation } from "react-router-dom";
import { useEffect, useState } from "react";

const PHASE_LABELS = {
  LOADING:        "Dip",
  SET_POINT:      "Set Point",
  FOLLOW_THROUGH: "Follow Through",
};

function Results() {
  const { state }  = useLocation();
  const file       = state?.file;

  const [loading, setLoading] = useState(true);
  const [results, setResults] = useState(null);
  const [error,   setError]   = useState(null);

  useEffect(() => {
    if (!file) {
      setLoading(false);
      setError("No video was provided.");
      return;
    }

    const upload = async () => {
      try {
        const formData = new FormData();
        formData.append("file", file);

        const res = await fetch("http://localhost:8000/upload-and-analyze", {
          method: "POST",
          body: formData,
        });

        if (!res.ok) throw new Error("Analysis failed.");

        const data = await res.json();
        setResults(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    upload();
  }, [file]);

  if (loading) return <h1>Analyzing your shot...</h1>;
  if (error)   return <h1>{error}</h1>;

  const { feedback, snapshots, overlay_url } = results;

  return (
    <div>
      <h1>Analysis Complete</h1>

      {overlay_url && (
        <video
          src={overlay_url}
          controls
          style={{ width: "100%", maxWidth: 640, borderRadius: 8 }}
        />
      )}

      <div style={{ display: "flex", gap: "24px", flexWrap: "wrap", marginTop: 32 }}>
        {Object.entries(snapshots).map(([phase, url]) => (
          <div key={phase}>
            <h3>{PHASE_LABELS[phase] || phase}</h3>
            <img src={url} alt={phase} style={{ width: 320, borderRadius: 8 }} />

            {feedback[phase] && (
              <ul>
                {Object.entries(feedback[phase]).map(([joint, info]) => (
                  <li key={joint} style={{ color: info.status === "good" ? "green" : "red" }}>
                    <strong>{joint}</strong>: {info.angle.toFixed(1)}° — {info.message}
                  </li>
                ))}
              </ul>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default Results;