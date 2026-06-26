import Navbar from "../components/Navbar";
import UploadHeader from "../components/UploadHeader";
import UploadInstructions from "../components/UploadInstructions";
import UploadSection from "../components/UploadSection";

function UploadPage() {
  return (
    <div>
      <Navbar />
      <UploadHeader />
      <UploadInstructions />

      <UploadSection />
    </div>
  );
}

export default UploadPage;