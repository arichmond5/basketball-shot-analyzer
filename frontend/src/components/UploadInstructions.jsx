import "./UploadInstructions.css";

function UploadInstructions() {
  return (
    <div className="upload-instructions">
      <h2>Recording Instructions</h2>

      <ul>
        <li>
          Position the camera on the shooting-arm side (your shooting arm should be closest to the camera).
        </li>

        <li>
          Keep your body parallel to the camera (side-view angle — no front or behind angles).
        </li>

        <li>
          Make sure your full body is visible in the frame from head to feet.
        </li>

        <li>
          Record only the shot attempt — start from the dip into the shooting motion.
        </li>

        <li>
          Do NOT include dribbling or movement before the shot. Only one shot per video.
        </li>

        <li>
          Keep the camera completely still (no panning or following the ball).
        </li>

        <li>
          The shooter must remain in frame the entire time.
        </li>

        <li>
          Only one person should be visible in the frame.
        </li>
      </ul>
    </div>
  );
}

export default UploadInstructions;