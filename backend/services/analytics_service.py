"""Analytics service for dashboard metrics."""

from datetime import datetime, timezone

from backend.app.database import get_database
from backend.app.repositories.scan_repository import SCAN_RESULTS_COLLECTION
from backend.models.schemas import AnalyticsSummaryResponse


class AnalyticsService:
    """Provides aggregate scan metrics from MongoDB."""

    async def get_summary(self) -> AnalyticsSummaryResponse:
        """Return real scan analytics from the url_scans collection."""

        collection = get_database()[SCAN_RESULTS_COLLECTION]
        total_scans = await collection.count_documents({})
        safe_count = await collection.count_documents({"prediction": {"$regex": "^Legitimate$", "$options": "i"}})
        phishing_count = await collection.count_documents({"prediction": {"$regex": "^Phishing$", "$options": "i"}})
        suspicious_count = await collection.count_documents({"risk_level": {"$regex": "^Medium$", "$options": "i"}})
        critical_count = await collection.count_documents({"risk_level": {"$regex": "^Critical$", "$options": "i"}})
        blocked_count = await collection.count_documents({"protection_action": "BLOCK"})
        daily_scans = await self._daily_scans(collection)

        return AnalyticsSummaryResponse(
            total_scans=total_scans,
            safe_count=safe_count,
            suspicious_count=suspicious_count,
            phishing_count=phishing_count,
            critical_count=critical_count,
            blocked_count=blocked_count,
            daily_scans=daily_scans,
            last_updated=datetime.now(timezone.utc),
        )

    async def _daily_scans(self, collection) -> list[dict[str, int | str]]:
        """Aggregate scan volume by day."""

        pipeline = [
            {
                "$group": {
                    "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$timestamp"}},
                    "count": {"$sum": 1},
                }
            },
            {"$sort": {"_id": 1}},
            {"$project": {"_id": 0, "date": "$_id", "count": 1}},
        ]
        return await collection.aggregate(pipeline).to_list(length=30)
