// Risk badge maps model risk levels into consistent visual states.
function RiskBadge({ riskLevel }) {
  const normalized = String(riskLevel || "Low").toLowerCase();
  const className = normalized.includes("high")
    ? "status-pill status-high"
    : normalized.includes("medium")
      ? "status-pill status-medium"
      : "status-pill status-low";

  return <span className={className}>{riskLevel || "Low"}</span>;
}

export default RiskBadge;

