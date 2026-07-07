import Navbar from "../components/Navbar/Navbar.jsx";
import Hero from "../components/Hero/Hero.jsx";
import HowItWorks from "../components/HowItWorks/HowItWorks.jsx";
import About from "../components/About/About.jsx";
import Footer from "../components/Footer/Footer.jsx";

function HomePage() {
  return (
    <>
      <Navbar />

      <Hero />

      <HowItWorks />

      <About />
      
      <Footer />
    </>
  );
}

export default HomePage;
