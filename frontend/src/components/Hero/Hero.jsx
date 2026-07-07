import "./Hero.css";
import { useNavigate } from "react-router-dom";

function Hero() {
  const navigate = useNavigate();

  return (
    <section className="hero" id="home">
      <div className="hero-content">
        <h1>Perfect Your Shot</h1>

        <p>
          Analyze your shooting mechanics and receive instant feedback.
        </p>

        <button
          className="uploadButton"
          onClick={() => navigate("/upload")}
        >
          Get Started
        </button>
      </div>
    </section>
  );
}

export default Hero;