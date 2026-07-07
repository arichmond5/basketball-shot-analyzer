import { useEffect, useState } from "react";

import "./ExpirationTimer.css";

function ExpirationTimer({ expiresAt, onExpire }) {
  const [timeLeft, setTimeLeft] = useState("");
  const [showWarning, setShowWarning] = useState(false);
  const [warningShown, setWarningShown] = useState(false);

  useEffect(() => {
    const updateTimer = () => {
      const difference = new Date(expiresAt) - new Date();

      if (difference <= 0) {
        setTimeLeft("Expired");
        onExpire();
        return;
      }

      const totalSeconds = Math.floor(difference / 1000);

      const minutes = Math.floor(totalSeconds / 60);
      const seconds = totalSeconds % 60;

      setTimeLeft(
        `${minutes}:${seconds.toString().padStart(2, "0")}`
      );

      // Show popup once when 5 minutes remain
      if (totalSeconds <= 300 && !warningShown) {
        setShowWarning(true);
        setWarningShown(true);
      }
    };

    updateTimer();

    const interval = setInterval(updateTimer, 1000);

    return () => clearInterval(interval);
  }, [expiresAt, warningShown, onExpire]);

  return (
    <>
      <div className="timer">
        ⏳ Session expires in {timeLeft}
      </div>

      {showWarning && (
        <div className="expiration-popup">
          <div className="popup-content">
            <h2>⚠️ Session Expiring Soon</h2>
            <p>
              Your results will be deleted in 5 minutes.
              Please save anything you need before they expire.
            </p>

            <button onClick={() => setShowWarning(false)}>
              Continue
            </button>
          </div>
        </div>
      )}
    </>
  );
}

export default ExpirationTimer;
