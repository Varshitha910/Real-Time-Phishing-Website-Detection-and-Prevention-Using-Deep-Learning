"""MongoDB persistence layer for phishing scan results.

This repository owns the `url_scans` collection. It stores each URL scan
with prediction output, confidence, risk level, timestamp, and SHAP explanation
data so the API, dashboard, and analytics modules can reuse one consistent
document shape.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import DESCENDING

from backend.app.database import get_database


SCAN_RESULTS_COLLECTION = "url_scans"
DEFAULT_HISTORY_LIMIT = 100
MAX_HISTORY_LIMIT = 1000


class ScanRepository:
    """Repository for creating, reading, and deleting URL scan records."""

    def __init__(self, collection: AsyncIOMotorCollection | None = None) -> None:
        self._collection = collection

    @property
    def collection(self) -> AsyncIOMotorCollection:
        """Return the MongoDB collection, resolving it lazily from the app DB."""

        if self._collection is not None:
            return self._collection
        return get_database()[SCAN_RESULTS_COLLECTION]

    async def save_scan_result(
        self,
        scan_result: dict[str, Any] | None = None,
        *,
        url: str | None = None,
        prediction: str | None = None,
        confidence: float | None = None,
        risk_level: str | None = None,
        shap_explanation: list[dict[str, Any]] | dict[str, Any] | None = None,
        features: dict[str, Any] | None = None,
        protection_action: str | None = None,
        timestamp: datetime | None = None,
    ) -> dict[str, Any]:
        """Save one scan result and return the stored document.

        Args:
            scan_result: Optional dictionary from the prediction pipeline.
            url: URL that was scanned.
            prediction: Model label, such as Phishing or Legitimate.
            confidence: Prediction confidence percentage.
            risk_level: Low, Medium, or High risk label.
            shap_explanation: SHAP explanation object or top-feature list.
            timestamp: Optional scan timestamp; current UTC time is used by default.
        """

        document = self._build_scan_document(
            scan_result=scan_result,
            url=url,
            prediction=prediction,
            confidence=confidence,
            risk_level=risk_level,
            shap_explanation=shap_explanation,
            features=features,
            protection_action=protection_action,
            timestamp=timestamp,
        )

        insert_result = await self.collection.insert_one(document)
        document["_id"] = insert_result.inserted_id
        return self._serialize_document(document)

    async def get_scan_history(self, limit: int = DEFAULT_HISTORY_LIMIT, skip: int = 0) -> list[dict[str, Any]]:
        """Return paginated scan history ordered from newest to oldest."""

        safe_limit = self._normalize_limit(limit)
        safe_skip = max(skip, 0)
        cursor = (
            self.collection.find({})
            .sort("timestamp", DESCENDING)
            .skip(safe_skip)
            .limit(safe_limit)
        )
        documents = await cursor.to_list(length=safe_limit)
        return [self._serialize_document(document) for document in documents]

    async def get_recent_scans(self, limit: int = 10) -> list[dict[str, Any]]:
        """Return the most recent scan records for dashboard widgets."""

        return await self.get_scan_history(limit=limit, skip=0)

    async def delete_scan(self, scan_id: str) -> bool:
        """Delete a scan record by MongoDB ObjectId string.

        Returns:
            True if a document was deleted, otherwise False.
        """

        object_id = self._parse_object_id(scan_id)
        delete_result = await self.collection.delete_one({"_id": object_id})
        return delete_result.deleted_count == 1

    def _build_scan_document(
        self,
        *,
        scan_result: dict[str, Any] | None,
        url: str | None,
        prediction: str | None,
        confidence: float | None,
        risk_level: str | None,
        shap_explanation: list[dict[str, Any]] | dict[str, Any] | None,
        features: dict[str, Any] | None,
        protection_action: str | None,
        timestamp: datetime | None,
    ) -> dict[str, Any]:
        """Normalize API/model output into a MongoDB-ready document."""

        source = scan_result or {}
        resolved_url = url or source.get("url")
        resolved_prediction = prediction or source.get("prediction")
        resolved_confidence = confidence if confidence is not None else source.get("confidence")
        resolved_risk_level = risk_level or source.get("risk_level")
        resolved_shap = (
            shap_explanation
            if shap_explanation is not None
            else source.get("shap_explanation", source.get("top_features", source.get("explanation", [])))
        )
        resolved_features = features if features is not None else source.get("features", {})
        resolved_action = protection_action or source.get("protection_action") or source.get("action")
        resolved_timestamp = timestamp or source.get("timestamp") or source.get("scanned_at") or datetime.now(timezone.utc)

        if not resolved_url:
            raise ValueError("Scan result must include a URL.")
        if not resolved_prediction:
            raise ValueError("Scan result must include a prediction.")
        if resolved_confidence is None:
            raise ValueError("Scan result must include confidence.")
        if not resolved_risk_level:
            raise ValueError("Scan result must include a risk level.")

        return {
            "url": str(resolved_url),
            "prediction": str(resolved_prediction),
            "confidence": float(resolved_confidence),
            "risk_level": str(resolved_risk_level),
            "timestamp": self._ensure_datetime(resolved_timestamp),
            "features": resolved_features or {},
            "shap_explanation": resolved_shap or [],
            "protection_action": str(resolved_action or ""),
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }

    def _serialize_document(self, document: dict[str, Any]) -> dict[str, Any]:
        """Convert MongoDB-specific values into API-friendly Python values."""

        serialized = document.copy()
        if "_id" in serialized:
            serialized["id"] = str(serialized.pop("_id"))

        for field in ("timestamp", "created_at", "updated_at"):
            if isinstance(serialized.get(field), datetime):
                serialized[field] = serialized[field].isoformat()

        return serialized

    def _parse_object_id(self, scan_id: str) -> ObjectId:
        """Validate and convert a string ID to MongoDB ObjectId."""

        if not ObjectId.is_valid(scan_id):
            raise ValueError(f"Invalid scan id: {scan_id}")
        return ObjectId(scan_id)

    def _normalize_limit(self, limit: int) -> int:
        """Keep query limits within a safe production range."""

        if limit <= 0:
            return DEFAULT_HISTORY_LIMIT
        return min(limit, MAX_HISTORY_LIMIT)

    def _ensure_datetime(self, value: Any) -> datetime:
        """Convert supported timestamp values into datetime objects."""

        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        raise ValueError("Timestamp must be a datetime or ISO datetime string.")


_default_repository = ScanRepository()


async def save_scan_result(*args: Any, **kwargs: Any) -> dict[str, Any]:
    """Module-level helper for saving a scan result."""

    return await _default_repository.save_scan_result(*args, **kwargs)


async def get_scan_history(limit: int = DEFAULT_HISTORY_LIMIT, skip: int = 0) -> list[dict[str, Any]]:
    """Module-level helper for reading paginated scan history."""

    return await _default_repository.get_scan_history(limit=limit, skip=skip)


async def get_recent_scans(limit: int = 10) -> list[dict[str, Any]]:
    """Module-level helper for reading the latest scan records."""

    return await _default_repository.get_recent_scans(limit=limit)


async def delete_scan(scan_id: str) -> bool:
    """Module-level helper for deleting a scan record."""

    return await _default_repository.delete_scan(scan_id)
