from __future__ import annotations
from typing import Any
from .common import GateDecision, base_gate_decision

class LaneSuccessorAdmissibilityGate:
    name = "LaneSuccessorAdmissibilityGate"
    action_type = "lane_successor_resolution"
    def evaluate(self, payload: dict[str, Any]) -> GateDecision:
        return base_gate_decision(self.name, self.action_type, payload)
