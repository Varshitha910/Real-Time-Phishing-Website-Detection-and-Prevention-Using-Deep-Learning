"""Routes for real-time phishing detection."""

from fastapi import APIRouter, HTTPException, status

from backend.models.schemas import DetectionRequest, DetectionResponse
from backend.services.detection_service import DetectionService
from backend.utils.validators import normalize_url, validate_url


router = APIRouter(prefix="/detect", tags=["Detection"])
service = DetectionService()


@router.post("", response_model=DetectionResponse)
async def detect_url(payload: DetectionRequest) -> DetectionResponse:
    """Analyze a URL and return its phishing risk prediction."""

    if not validate_url(str(payload.url)):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="The supplied URL is not valid.",
        )

    normalized_url = normalize_url(str(payload.url))
    return await service.detect(normalized_url, source=payload.source)

