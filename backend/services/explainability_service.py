"""Explainable AI service.

The production version should load a SHAP explainer and background dataset.
This starter version formats deterministic feature reasons so the API and UI
can be developed before the trained model is available.
"""

from backend.models.schemas import ExplanationRequest, ExplanationResponse, FeatureContribution, RiskLevel


class ExplainabilityService:
    """Generates human-readable reasons for a phishing prediction."""

    def explain(self, request: ExplanationRequest) -> ExplanationResponse:
        """Explain a prediction from provided feature values."""

        risk_level = request.risk_level or RiskLevel.SUSPICIOUS
        contributions = self.explain_features(request.features, risk_level)
        return ExplanationResponse(
            url=request.url,
            risk_level=risk_level,
            top_contributions=contributions,
            narrative=self._build_narrative(contributions, risk_level),
        )

    def explain_features(
        self,
        features: dict[str, float | int | bool],
        risk_level: RiskLevel,
    ) -> list[FeatureContribution]:
        """Create starter feature contributions from extracted URL features."""

        reasons: list[FeatureContribution] = []

        if features.get("url_length", 0) > 75:
            reasons.append(FeatureContribution(feature="url_length", impact=0.22, description="URL is unusually long."))
        if features.get("has_ip_address") or features.get("ip_address_present"):
            reasons.append(FeatureContribution(feature="ip_address_present", impact=0.20, description="URL uses an IP address instead of a domain."))
        if features.get("subdomain_count", 0) > 2:
            reasons.append(FeatureContribution(feature="subdomain_count", impact=0.16, description="URL contains multiple subdomains."))
        if not features.get("uses_https", bool(features.get("https_available", 1))):
            reasons.append(FeatureContribution(feature="https_available", impact=0.15, description="URL does not use HTTPS."))
        keyword_count = features.get("suspicious_keyword_count", features.get("suspicious_word_count", 0))
        if keyword_count > 0:
            reasons.append(FeatureContribution(feature="suspicious_word_count", impact=0.12, description="URL contains phishing-related keywords."))

        if not reasons:
            reasons.append(
                FeatureContribution(
                    feature="baseline",
                    impact=0.01,
                    description=f"No dominant high-risk feature was found for this {risk_level.value} result.",
                )
            )

        return reasons[:5]

    def _build_narrative(self, contributions: list[FeatureContribution], risk_level: RiskLevel) -> str:
        """Summarize the most important reasons in one sentence."""

        feature_text = ", ".join(item.description for item in contributions[:3])
        return f"The URL was classified as {risk_level.value} because: {feature_text}"
