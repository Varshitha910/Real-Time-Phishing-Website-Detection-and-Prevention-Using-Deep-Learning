"""Request and response schemas shared by routes and services."""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, HttpUrl


class RiskLevel(str,Enum):
    """Supported URL risk levels."""

    SAFE = "safe"
    SUSPICIOUS = "suspicious"
    PHISHING = "phishing"
    CRITICAL = "critical"


class PreventionAction(str,Enum):
    """Actions the prevention engine can send to the browser extension."""

    ALLOW = "allow"
    WARN = "warn"
    WARN_AND_BLOCK = "warn_and_block"
    BLOCK = "block"


class FeatureContribution(BaseModel):
    """A single feature explanation item, compatible with future SHAP output."""

    feature: str
    impact: float
    description: str


class DetectionRequest(BaseModel):
    """Payload for a URL scan request."""

    url: HttpUrl
    source: str = Field(default="api", description="Origin of the scan, such as api, dashboard, or extension.")


class DetectionResponse(BaseModel):
    """Full result returned after analyzing a URL."""

    url: str
    prediction: str
    confidence_score: float
    risk_level: RiskLevel
    prevention_action: PreventionAction
    explanation: list[FeatureContribution]
    features: dict[str, Any]
    summary: str
    source: str
    scanned_at: datetime


class PreventionRequest(BaseModel):
    """Input for converting risk into a prevention action."""

    url: str
    risk_level: RiskLevel
    confidence_score: float = Field(ge=0.0, le=1.0)


class PreventionResponse(BaseModel):
    """Prevention decision returned to the dashboard or Chrome extension."""

    url: str
    risk_level: RiskLevel
    confidence_score: float
    action: PreventionAction
    message: str


class ExplanationRequest(BaseModel):
    """Input for explaining a model prediction."""

    url: str
    features: dict[str, Any]
    risk_level: RiskLevel | None = None


class ExplanationResponse(BaseModel):
    """Explanation response formatted for the UI."""

    url: str
    risk_level: RiskLevel
    top_contributions: list[FeatureContribution]
    narrative: str


class AnalyticsSummaryResponse(BaseModel):
    """Dashboard summary metrics."""

    total_scans: int
    safe_count: int
    suspicious_count: int
    phishing_count: int
    critical_count: int
    blocked_count: int = 0
    daily_scans: list[dict[str, Any]] = Field(default_factory=list)
    last_updated: datetime
