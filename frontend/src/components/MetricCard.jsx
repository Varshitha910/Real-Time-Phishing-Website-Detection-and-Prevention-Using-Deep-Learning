// Compact metric display used on the dashboard and analytics pages.
function MetricCard({ label, value }) {
  return (
    <section className="card" aria-label={label}>
      <div className="metric-label">{label}</div>
      <div className="metric-value">{value}</div>
    </section>
  );
}

export default MetricCard;

