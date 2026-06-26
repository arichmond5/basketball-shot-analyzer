import Navbar from "../components/Navbar.jsx";
import Hero from "../components/Hero.jsx";
import HowItWorks from "../components/HowItWorks.jsx";
import About from "../components/About.jsx";
import Footer from "../components/Footer.jsx";

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