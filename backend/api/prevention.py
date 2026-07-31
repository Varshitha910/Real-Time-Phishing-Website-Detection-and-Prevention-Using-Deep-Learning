"""Routes for prevention decisions such as allow, warn, or block."""

from fastapi import APIRouter

from backend.models.schemas import PreventionRequest, PreventionResponse
from backend.services.prevention_service import PreventionService


router = APIRouter(prefix="/prevention", tags=["Prevention"])
service = PreventionService()


@router.post("/decision", response_model=PreventionResponse)
async def prevention_decision(payload: PreventionRequest) -> PreventionResponse:
    """Convert model risk into a browser-facing prevention action."""

    return service.decide(payload)

