"""Tests for the starter detection workflow."""

import pytest

from backend.models.schemas import RiskLevel
from backend.services.detection_service import DetectionService


@pytest.mark.asyncio
async def test_detection_service_returns_response() -> None:
    """Detection should return a complete response object."""

    service = DetectionService()
    result = await service.detect("http://192.168.1.10/login/verify", source="test")

    assert result.url == "http://192.168.1.10/login/verify"
    assert result.risk_level in {RiskLevel.SUSPICIOUS, RiskLevel.PHISHING, RiskLevel.CRITICAL}
    assert result.explanation

