import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import UploadSection from "./components/UploadSection";
import HowItWorks from "./components/HowItWorks";
import Results from "./components/Results";
import About from "./components/About";
import Footer from "./components/Footer";

function App() {
  return (
    <>
      <Navbar />
      <Hero />
      <UploadSection />
      <HowItWorks />
      <Results />
      <About />
      <Footer />
    </>
  );
}

export default App;