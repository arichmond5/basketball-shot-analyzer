import "./UploadExample.css";

function UploadExample() {
  return (
    <div className="upload-example">
      <h2>Example Video</h2>

      <video
        controls
        width="600"
        src="/exampleVideo.mov"
      >
        Your browser does not support the video tag.
      </video>
    </div>
  );
}

export default UploadExample;