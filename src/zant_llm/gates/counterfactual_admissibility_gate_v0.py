from __future__ import annotations

from typing import Any

from .common import GateDecision, contains_forbidden_key, evaluate_readiness_vector


class CounterfactualAdmissibilityGate:
    name = "CounterfactualAdmissibilityGate"
    action_type = "counterfactual_explanation"

    def evaluate(self, payload: dict[str, Any]) -> GateDecision:
        readiness = dict(payload.get("readiness_vector", {}))
        readiness.setdefault("authority_boundary_declared", payload.get("runtime_authority_granted") is False)
        readiness.setdefault("provider_dispatch_disabled", payload.get("provider_dispatch_enabled") is False)
        if not payload.get("counterfactual_only", False):
            readiness["counterfactual_marked_explanation_only"] = False
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
