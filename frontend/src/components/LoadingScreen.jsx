import "./LoadingScreen.css";

function LoadingScreen() {
  return (
    <div className="loading-screen">
      <div className="spinner"></div>

      <h1>Analyzing your shot...</h1>

      <p>This usually takes a few seconds.</p>
    </div>
  );
}

export default LoadingScreen;