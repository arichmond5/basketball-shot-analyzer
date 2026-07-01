import { useLocation } from "react-router-dom";

import useShotAnalysis from "../hooks/useShotAnalysis";

import Navbar from "../components/Navbar";
import ResultsHeader from "../components/ResultsHeader";
import LoadingScreen from "../components/LoadingScreen";
import ResultsBreakdown from "../components/ResultsBreakdown";

function Results() {
  const { state } = useLocation();
  const file = state?.file;

  // 🚨 guard: prevents hook from breaking if no file passed
  if (!file) {
    return <h1>No file provided</h1>;
  }

  const { loading, error, results } = useShotAnalysis(file);

  if (loading) return <LoadingScreen />;
  if (error) return <h1>{error}</h1>;

  // 🚨 guard: prevents destructuring crash
  if (!results) return <LoadingScreen />;

  const { feedback = {}, snapshots = {}, overlay_url } = results;

  return (
    <div>
      <Navbar />

      <ResultsHeader url={overlay_url} />

      <ResultsBreakdown
        snapshots={snapshots}
        feedback={feedback}
      />
    </div>
  );
}

export default Results;