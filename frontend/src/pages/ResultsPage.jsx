import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";

import Navbar from "../components/Navbar/Navbar";
import LoadingScreen from "../components/LoadingScreen/LoadingScreen";
import ResultsHeader from "../components/ResultsHeader/ResultsHeader";
import ResultsBreakdown from "../components/ResultsBreakdown/ResultsBreakdown";
import DownloadResults from "../components/DownloadResults/DownloadResults";
import ExpirationTimer from "../components/ExpirationTimer/ExpirationTimer";
import ExpiredSession from "../components/ExpiredSession/ExpiredSession";
import NotFound from "./ErrorPage";

const API_URL = import.meta.env.VITE_API_URL;

function ResultsPage() {
  const { jobId } = useParams();

  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [expired, setExpired] = useState(false);

  useEffect(() => {
    let interval = null;

    const fetchResults = async () => {
      try {
        const res = await fetch(
          `${API_URL}/results/${jobId}`
        );

        if (res.status === 404) {
          setError("not_found");
          clearInterval(interval);
          return;
        }

        if (!res.ok) {
          throw new Error("Failed to load results");
        }

        const data = await res.json();
        setResults(data);

        if (data.status === "done") {
          clearInterval(interval);
        }

      } catch (err) {
        setError(err.message);
        clearInterval(interval);
      }
    };

    // Fetch immediately
    fetchResults();

    // Continue checking status
    interval = setInterval(fetchResults, 1500);

    return () => {
      clearInterval(interval);
    };

  }, [jobId]);

  if (expired) {
    return <ExpiredSession />;
  }

  if (error === "not_found") {
    return <NotFound />;
  }

  if (error) {
    return <h1>{error}</h1>;
  }

  if (!results || results.status !== "done") {
    return <LoadingScreen />;
  }

  const {
    feedback = {},
    snapshots = {},
    overlay_url
  } = results;

  return (
    <div>
      <Navbar />

      {results.expires_at && (
        <ExpirationTimer
          expiresAt={results.expires_at}
          onExpire={() => setExpired(true)}
        />
      )}

      <ResultsHeader url={overlay_url} />

      <ResultsBreakdown
        snapshots={snapshots}
        feedback={feedback}
      />

      <DownloadResults jobId={jobId} />
    </div>
  );
}

export default ResultsPage;
