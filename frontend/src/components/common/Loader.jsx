function LoadingOverlay() {
  return (
    <div className="overlay">
      <div className="ring-loader"></div>
      <p className="overlay-text">Initializing Security Engine...</p>
    </div>
  );
}

export default LoadingOverlay;