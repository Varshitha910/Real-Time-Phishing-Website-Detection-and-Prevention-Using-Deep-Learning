"""Prediction threshold management."""

from enum import StrEnum


class ModelRiskLevel(StrEnum):
    """Risk levels produced during model inference."""

    SAFE = "safe"
    SUSPICIOUS = "suspicious"
    PHISHING = "phishing"
    CRITICAL = "critical"


def risk_from_score(score: float, suspicious_threshold: float = 0.45, phishing_threshold: float = 0.75) -> ModelRiskLevel:
    """Convert a model score into a risk level."""

    if score >= 0.9:
        return ModelRiskLevel.CRITICAL
    if score >= phishing_threshold:
        return ModelRiskLevel.PHISHING
    if score >= suspicious_threshold:
        return ModelRiskLevel.SUSPICIOUS
    return ModelRiskLevel.SAFE

