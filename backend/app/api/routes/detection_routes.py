"""FastAPI routes for real-time phishing prediction.

This router exposes POST /predict. It validates URL input, calls the trained
machine learning predictor, and returns a compact response suitable for the
React dashboard or Chrome extension.
"""

from __future__ import annotations

from urllib.parse import urlparse

from fastapi import APIRouter, HTTPException, status
from typing import Any

from pydantic import BaseModel, Field


router = APIRouter(tags=["Detection"])


class PredictionRequest(BaseModel):
    """Request body for phishing prediction."""

    url: str = Field(..., description="Full URL to analyze, including http:// or https://")


class PredictionResponse(BaseModel):
    """Response body returned after model inference."""

    url: str | None = None
    prediction: str = Field(..., examples=["Phishing"])
    confidence: float = Field(..., ge=0.0, le=100.0, examples=[95.2])
    risk_level: str = Field(..., examples=["High"])
    features: dict[str, Any] = Field(default_factory=dict)
    explanation: list[dict[str, Any]] = Field(default_factory=list)
    protection: dict[str, str] = Field(default_factory=dict)


@router.post("/predict", response_model=PredictionResponse, status_code=status.HTTP_200_OK)
async def predict_phishing_url(request: PredictionRequest) -> PredictionResponse:
    """Validate a URL and return phishing prediction, confidence, and risk level."""

    url = request.url.strip() if request.url else ""
    _validate_url_or_raise(url)

    try:
        # Import lazily so model/dependency issues become controlled HTTP errors.
        from backend.app.repositories.scan_repository import save_scan_result
        from backend.ml.model_loader import predict_url
        from backend.models.schemas import RiskLevel
        from backend.services.explainability_service import ExplainabilityService
        from backend.services.protection_service import decide_protection

        prediction_result = predict_url(url)
        protection = decide_protection(str(prediction_result["url"]), str(prediction_result["risk_level"]))
        explanation_models = ExplainabilityService().explain_features(
            prediction_result["features"],
            _schema_risk(str(prediction_result["risk_level"])),
        )
        explanation = [_dump_model(item) for item in explanation_models]

        await save_scan_result(
            url=str(prediction_result["url"]),
            prediction=str(prediction_result["prediction"]),
            confidence=float(prediction_result["confidence"]),
            risk_level=str(prediction_result["risk_level"]),
            shap_explanation=explanation,
            features=prediction_result["features"],
            protection_action=protection["action"],
        )
    except (ImportError, ModuleNotFoundError, FileNotFoundError, OSError) as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Prediction model is not available: {exc}",
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {exc}",
        ) from exc

    return PredictionResponse(
        url=str(prediction_result["url"]),
        prediction=str(prediction_result["prediction"]),
        confidence=float(prediction_result["confidence"]),
        risk_level=str(prediction_result["risk_level"]),
        features=prediction_result["features"],
        explanation=explanation,
        protection=protection,
    )


def _validate_url_or_raise(url: str) -> None:
    """Validate URL input and raise HTTP errors with clear status codes."""

    if not url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="URL cannot be empty.",
        )

    parsed_url = urlparse(url)
    if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid URL. Provide a full URL beginning with http:// or https://.",
        )


def _schema_risk(risk_level: str):
    """Map public risk labels to the internal explanation enum."""

    from backend.models.schemas import RiskLevel

    if risk_level == "Critical":
        return RiskLevel.CRITICAL
    if risk_level == "High":
        return RiskLevel.PHISHING
    if risk_level == "Medium":
        return RiskLevel.SUSPICIOUS
    return RiskLevel.SAFE


def _dump_model(item) -> dict[str, Any]:
    """Serialize Pydantic models across v1 and v2."""

    if hasattr(item, "model_dump"):
        return item.model_dump()
    return item.dict()
