from __future__ import annotations
from typing import Any
from .common import GateDecision, base_gate_decision

class TrainingSampleAdmissibilityGate:
    name = "TrainingSampleAdmissibilityGate"
    action_type = "training_sample_acceptance"
    def evaluate(self, payload: dict[str, Any]) -> GateDecision:
        return base_gate_decision(self.name, self.action_type, payload)
