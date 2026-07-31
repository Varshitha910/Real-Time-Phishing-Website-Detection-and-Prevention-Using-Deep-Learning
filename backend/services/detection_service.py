"""Real-time URL detection service using the trained ML model."""

from datetime import datetime, timezone

from backend.app.repositories.scan_repository import save_scan_result
from backend.ml.model_loader import predict_url
from backend.models.schemas import DetectionResponse, FeatureContribution, PreventionAction, RiskLevel
from backend.services.explainability_service import ExplainabilityService
from backend.services.protection_service import decide_protection
from backend.utils.response_formatter import build_detection_summary


class DetectionService:
    """Coordinates feature extraction, prediction, explanation, and action."""

    def __init__(self) -> None:
        self.explainer = ExplainabilityService()

    async def detect(self, url: str, source: str = "api") -> DetectionResponse:
        """Run trained-model phishing detection and persist the scan."""

        model_result = predict_url(url)
        features = model_result["features"]
        risk_label = str(model_result["risk_level"])
        risk_level = self._schema_risk(risk_label)
        protection = decide_protection(str(model_result["url"]), risk_label)
        explanation = self.explainer.explain_features(features, risk_level)
        scanned_at = datetime.now(timezone.utc)

        await save_scan_result(
            url=str(model_result["url"]),
            prediction=str(model_result["prediction"]),
            confidence=float(model_result["confidence"]),
            risk_level=risk_label,
            shap_explanation=[self._dump_explanation(item) for item in explanation],
            features=features,
            protection_action=protection["action"],
            timestamp=scanned_at,
        )

        return DetectionResponse(
            url=str(model_result["url"]),
            prediction=str(model_result["prediction"]),
            confidence_score=float(model_result["confidence"]),
            risk_level=risk_level,
            prevention_action=self._schema_action(protection["action"], risk_level),
            explanation=explanation,
            features=features,
            summary=build_detection_summary(str(model_result["url"]), risk_level, float(model_result["confidence"])),
            source=source,
            scanned_at=scanned_at,
        )

    def _schema_risk(self, risk_label: str) -> RiskLevel:
        """Map public risk labels to the existing API enum."""

        if risk_label == "Critical":
            return RiskLevel.CRITICAL
        if risk_label == "High":
            return RiskLevel.PHISHING
        if risk_label == "Medium":
            return RiskLevel.SUSPICIOUS
        return RiskLevel.SAFE

    def _schema_action(self, action: str, risk_level: RiskLevel) -> PreventionAction:
        """Map protection action to the existing prevention enum."""

        if action == "BLOCK":
            return PreventionAction.BLOCK
        if action == "WARN" and risk_level == RiskLevel.PHISHING:
            return PreventionAction.WARN_AND_BLOCK
        if action == "WARN":
            return PreventionAction.WARN
        return PreventionAction.ALLOW

    def _dump_explanation(self, item: FeatureContribution) -> dict:
        """Serialize explanation models across Pydantic versions."""

        if hasattr(item, "model_dump"):
            return item.model_dump()
        return item.dict()
