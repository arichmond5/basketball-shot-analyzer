import { useLocation } from "react-router-dom";
import { useEffect } from "react";

function Results() {
  const { state } = useLocation();
  const file = state?.file;

  useEffect(() => {
    if (!file) return;

    const upload = async () => {
      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch("http://localhost:8000/upload-and-analyze", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();

      console.log(data);
    };

    upload();
  }, [file]);

  return <>
  <h1>Analyzing your shot...</h1>
  
  </>;

}

export default Results;