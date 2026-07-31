"""Prevention engine for browser and dashboard decisions."""

from backend.models.schemas import PreventionRequest, PreventionResponse, PreventionAction, RiskLevel


class PreventionService:
    """Maps risk levels to actions that protect users in real time."""

    def decide(self, request: PreventionRequest) -> PreventionResponse:
        """Return an action for the provided risk level and confidence."""

        action = self.action_for_risk(request.risk_level)
        message = self.message_for_action(action)
        return PreventionResponse(
            url=request.url,
            risk_level=request.risk_level,
            confidence_score=request.confidence_score,
            action=action,
            message=message,
        )

    def action_for_risk(self, risk_level: RiskLevel) -> PreventionAction:
        """Choose the browser behavior for a model risk level."""

        if risk_level == RiskLevel.CRITICAL:
            return PreventionAction.BLOCK
        if risk_level == RiskLevel.PHISHING:
            return PreventionAction.WARN_AND_BLOCK
        if risk_level == RiskLevel.SUSPICIOUS:
            return PreventionAction.WARN
        return PreventionAction.ALLOW

    def message_for_action(self, action: PreventionAction) -> str:
        """Return user-readable guidance for the chosen action."""

        messages = {
            PreventionAction.ALLOW: "No strong phishing indicators were detected.",
            PreventionAction.WARN: "This page has suspicious signals. Review it carefully before sharing information.",
            PreventionAction.WARN_AND_BLOCK: "This page is likely phishing and should be blocked.",
            PreventionAction.BLOCK: "This page shows critical phishing indicators and has been blocked.",
        }
        return messages[action]

