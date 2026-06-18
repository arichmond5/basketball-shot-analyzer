import "./About.css";

function About() {
  return (
    <section className="about" id="about">
        <h2>About</h2>
        
      <div className="about-card">

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