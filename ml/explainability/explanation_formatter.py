"""Human-readable explanation formatting."""


def format_explanation(top_features: list[dict[str, float | str]]) -> str:
    """Convert top feature impacts into a concise sentence."""

    if not top_features:
        return "No dominant feature contribution was identified for this prediction."

    feature_names = ", ".join(str(item["feature"]) for item in top_features[:3])
    return f"The prediction was mainly influenced by: {feature_names}."

