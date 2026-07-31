"""Helpers that turn technical results into readable API text."""

from backend.models.schemas import RiskLevel


def build_detection_summary(url: str, risk_level: RiskLevel, confidence: float) -> str:
    """Create a concise detection summary for dashboards and extension popups."""

    percent = round(confidence if confidence > 1 else confidence * 100, 2)
    return f"{url} is classified as {risk_level.value} with {percent}% model confidence."
