// Displays the latest URL prediction returned by the FastAPI backend.
import RiskBadge from "./RiskBadge.jsx";

function ScanResultCard({ result }) {
  if (!result) {
    return (
      <section className="card">
        <p className="muted">Submit a URL to see the model prediction.</p>
      </section>
    );
  }

  return (
    <section className="card">
      <h2>Scan Result</h2>
      <p>
        <strong>Prediction:</strong> {result.prediction}
      </p>
      <p>
        <strong>Confidence:</strong> {result.confidence}%
      </p>
      <p>
        <strong>Risk Level:</strong> <RiskBadge riskLevel={result.risk_level} />
      </p>
    </section>
  );
}

export default ScanResultCard;

