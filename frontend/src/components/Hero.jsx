import heroImage from "../assets/heroImage.webp";
import "./Hero.css";

function Hero() {
  return (
    <section
      className="hero"
      style={{
        backgroundImage: `
          linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)),
          url(${heroImage})
        `
      }}
    >
      <div className="hero-content">
        <h1>Perfect Your Shot</h1>
        <p>Analyze your shooting mechanics and receive instant feedback.</p>
        <button className="uploadButton">Upload Now</button>
      </div>
    </section>
  );
}

export default Hero;