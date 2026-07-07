import "./HowItWorks.css"

function HowItWorks() {
  return (
    <section className="how-it-works" id="how-it-works">
      <h2>How it works</h2>

      <div className="steps">
        <div className="step">
          <h3>Upload Your Shot</h3>
          <p>Upload a video of your basketball jump shot.</p>
          <img src="/UploadPhoto.jpeg" alt="Upload your shot" />
        </div>

        <div className="step">
          <h3>AI Movement Tracking</h3>
          <p>
            The system detects your body keypoints using computer vision
            to map your shooting form.
          </p>
          <img src="/AnalysisPhoto.jpeg" alt="AI movement tracking" />
        </div>

        <div className="step">
          <h3>Get Instant Feedback</h3>
          <p>
            Receive breakdown of your shooting mechanics and improvement tips.
          </p>
          <img src="/FeedbackPhoto.png" alt="Feedback dashboard" />
        </div>
      </div>
    </section>
  );
}

export default HowItWorks;
