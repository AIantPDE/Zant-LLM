from __future__ import annotations
 v0.4-evidence-gated-explanation-admissibility
from typing import Any
from .common import GateDecision, base_gate_decision

class FollowUpAdmissibilityGate:
    name = "FollowUpAdmissibilityGate"
    action_type = "followup_output"
    def evaluate(self, payload: dict[str, Any]) -> GateDecision:
        return base_gate_decision(self.name, self.action_type, payload)


from typing import Any

from .common import GateDecision, contains_forbidden_key, evaluate_readiness_vector


class FollowUpAdmissibilityGate:
    name = "FollowUpAdmissibilityGate"
    action_type = "followup_answer"

    def evaluate(self, payload: dict[str, Any]) -> GateDecision:
        readiness = dict(payload.get("readiness_vector", {}))
        readiness.setdefault("authority_boundary_declared", payload.get("runtime_authority_granted") is False)
        readiness.setdefault("provider_dispatch_disabled", payload.get("provider_dispatch_enabled") is False)
        if payload.get("asks_for_runtime_action"):
            readiness["followup_is_explanation_only"] = False
        decision, missing = evaluate_readiness_vector(readiness)
        return GateDecision(
            gate_name=self.name,
            action_type=self.action_type,
            decision=decision,
            readiness_vector=readiness,
            missing_evidence=missing,
            blocking_residuals=missing,
            reason="ready" if decision == "READY" else "missing evidence or admissibility residuals",
        )
 v0.1-explanation-preview-baseline
