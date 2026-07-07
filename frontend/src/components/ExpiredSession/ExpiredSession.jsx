import Navbar from "../Navbar/Navbar";
import "./ExpiredSession.css";

function ExpiredSession() {
  return (
    <div className="expired-page">
      <Navbar />

      <div className="expired-message">
        <h1>⚠️ Results not found</h1>
        <p>
          These results are no longer available or the link is invalid.
          Please upload your video again.
        </p>
      </div>
    </div>
  );
}

export default ExpiredSession;
