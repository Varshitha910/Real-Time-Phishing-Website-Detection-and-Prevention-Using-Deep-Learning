"""Tests for prevention action mapping."""

from backend.models.schemas import PreventionAction, RiskLevel
from backend.services.prevention_service import PreventionService


def test_critical_risk_is_blocked() -> None:
    """Critical URLs should be blocked by default."""

    service = PreventionService()
    assert service.action_for_risk(RiskLevel.CRITICAL) == PreventionAction.BLOCK


def test_safe_risk_is_allowed() -> None:
    """Safe URLs should be allowed by default."""

    service = PreventionService()
    assert service.action_for_risk(RiskLevel.SAFE) == PreventionAction.ALLOW

