from __future__ import annotations
from typing import Any
from .common import GateDecision, base_gate_decision

class FollowUpAdmissibilityGate:
    name = "FollowUpAdmissibilityGate"
    action_type = "followup_output"
    def evaluate(self, payload: dict[str, Any]) -> GateDecision:
        return base_gate_decision(self.name, self.action_type, payload)
