export default function Loader() {
  return (
    <div className="review-loading">
      <div className="spinner-ring" />
      <p className="loading-text">
        Analyzing your code
        <span className="loading-dots">
          <span>.</span><span>.</span><span>.</span>
        </span>
      </p>
    </div>
  );
}
