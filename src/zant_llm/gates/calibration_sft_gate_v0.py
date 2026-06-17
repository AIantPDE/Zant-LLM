from __future__ import annotations
from dataclasses import dataclass
from typing import Any

FORBIDDEN = {"runtime_authority_granted", "provider_dispatch_enabled", "new_decision_created", "writeback_execution", "worker_trigger", "tool_dispatch"}
ALLOWED = {"READY", "BLOCKED", "CLOSEOUT", "FAILCLOSED"}

@dataclass
class GateDecision:
    decision: str
    reason: str

class CalibrationSFTGate:
    name = "CalibrationSFTGate"

    def evaluate(self, case: dict[str, Any]) -> GateDecision:
        expected = case.get("expected_decision")
        if expected not in ALLOWED:
            return GateDecision("FAILCLOSED", "invalid expected decision")
        target = case.get("target", {})
        text = str(target)
        for k in FORBIDDEN:
            if f"'{k}': True" in text or f'"{k}": true' in text.lower():
                return GateDecision("FAILCLOSED", f"forbidden true field: {k}")
        return GateDecision(expected, "calibration sft case admissible")
