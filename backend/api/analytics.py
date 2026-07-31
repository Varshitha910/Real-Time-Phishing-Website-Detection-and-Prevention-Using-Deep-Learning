"""Routes for dashboard analytics and recent scan activity."""

from fastapi import APIRouter

from backend.models.schemas import AnalyticsSummaryResponse
from backend.services.analytics_service import AnalyticsService


router = APIRouter(prefix="/analytics", tags=["Analytics"])
service = AnalyticsService()


@router.get("/summary", response_model=AnalyticsSummaryResponse)
async def analytics_summary() -> AnalyticsSummaryResponse:
    """Return starter aggregate metrics for the React dashboard."""

    return await service.get_summary()


@router.get("", response_model=AnalyticsSummaryResponse)
async def analytics_summary_alias() -> AnalyticsSummaryResponse:
    """Return analytics summary from the base analytics route."""

    return await service.get_summary()
