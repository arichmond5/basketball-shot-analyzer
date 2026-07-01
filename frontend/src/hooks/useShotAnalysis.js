import { useEffect, useState } from "react";

export default function useShotAnalysis(file) {
  const [loading, setLoading] = useState(true);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

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

  return {
    loading,
    error,
    results,
  };
}