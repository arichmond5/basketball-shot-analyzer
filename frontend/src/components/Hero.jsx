import { useRef } from "react";
import "./Hero.css";
import UploadSection from "./UploadSection";"./UploadSection.jsx"

function Hero() {
  const fileInputRef = useRef(null);

  return (
    <section className="hero" id="home">
      <div className="hero-content">
        <h1>Perfect Your Shot</h1>

        <p>
          Analyze your shooting mechanics and receive instant feedback.
        </p>

        <UploadSection />
      </div>
    </section>
  );
}

export default Hero;