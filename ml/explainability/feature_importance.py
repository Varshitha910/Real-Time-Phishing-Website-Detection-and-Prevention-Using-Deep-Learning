"""Feature importance formatting helpers."""


def top_feature_importance(feature_names: list[str], impacts: list[float], limit: int = 5) -> list[dict[str, float | str]]:
    """Return the strongest feature impacts sorted by absolute contribution."""

    pairs = [{"feature": name, "impact": float(impact)} for name, impact in zip(feature_names, impacts, strict=False)]
    return sorted(pairs, key=lambda item: abs(float(item["impact"])), reverse=True)[:limit]

