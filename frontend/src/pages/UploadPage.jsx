import Navbar from "../components/Navbar";
import UploadExample from "../components/UploadExample";
import UploadHeader from "../components/UploadHeader";
import UploadInstructions from "../components/UploadInstructions";
import UploadSection from "../components/UploadSection";

function UploadPage() {
  return (
    <div>
      <Navbar />
      <UploadHeader />
      <UploadInstructions />
      <UploadExample />
      <UploadSection />
    </div>
  );
}

export default UploadPage;