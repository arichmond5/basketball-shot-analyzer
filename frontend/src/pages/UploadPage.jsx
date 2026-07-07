import Navbar from "../components/Navbar/Navbar";
import UploadExample from "../components/UploadExample/UploadExample";
import UploadHeader from "../components/UploadHeader/UploadHeader";
import UploadInstructions from "../components/UploadInstructions/UploadInstructions";
import UploadSection from "../components/UploadSection/UploadSection";

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
