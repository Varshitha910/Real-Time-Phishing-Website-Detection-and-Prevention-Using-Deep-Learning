"""Real-time browser protection decisions from model risk levels."""

from __future__ import annotations


def decide_protection(url: str, risk_level: str) -> dict[str, str]:
    """Return ALLOW, WARN, or BLOCK for a scanned URL."""

    normalized_risk = str(risk_level).lower()
    if normalized_risk == "critical":
        return {"url": url, "action": "BLOCK", "reason": "Critical phishing probability detected."}
    if normalized_risk == "high":
        return {"url": url, "action": "WARN", "reason": "High phishing risk detected. Show a strong browser warning."}
    if normalized_risk == "medium":
        return {"url": url, "action": "WARN", "reason": "Suspicious URL indicators detected. Warn the user."}
    return {"url": url, "action": "ALLOW", "reason": "Low phishing risk. Allow navigation."}
