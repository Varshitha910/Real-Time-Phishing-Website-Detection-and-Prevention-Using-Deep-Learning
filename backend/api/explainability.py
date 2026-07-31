"""Routes for SHAP-style model explanations."""

from fastapi import APIRouter

from backend.models.schemas import ExplanationRequest, ExplanationResponse
from backend.services.explainability_service import ExplainabilityService


router = APIRouter(prefix="/explain", tags=["Explainability"])
service = ExplainabilityService()


@router.post("", response_model=ExplanationResponse)
async def explain_prediction(payload: ExplanationRequest) -> ExplanationResponse:
    """Return the top feature reasons behind a phishing prediction."""

    return service.explain(payload)

