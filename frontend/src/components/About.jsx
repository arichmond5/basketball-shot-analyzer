import "./About.css";

function About() {
  return (
    <section className="about">
      <div className="about-card">
        <h2>About</h2>

        <p>
          This application helps basketball players improve their shooting form using computer vision and movement analysis.
        </p>

        <p>
          It detects key body mechanics such as posture, balance, and release timing to provide actionable feedback.
        </p>

        <p>
          Built to make shot analysis accessible to every player.
        </p>
      </div>
    </section>
  );
}

export default About;