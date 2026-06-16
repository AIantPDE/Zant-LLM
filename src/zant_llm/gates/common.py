from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

FORBIDDEN_OUTPUT_FIELDS = {
    "agent_action",
    "execution_action",
    "fetch_decision",
    "model_call",
    "provider_dispatch",
    "provider_registry_update",
    "remote_api_call",
    "route_decision",
    "runtime_authority",
    "runtime_authority_granted",
    "side_effect",
    "worker_trigger",
    "writeback_execution",
    "new_decision",
    "decision_override",
    "policy_update",
    "order_placement",
}

@dataclass
class GateDecision:
    gate_name: str
    action_type: str
    decision: str
    readiness_vector: dict[str, Any]
    missing_evidence: list[str] = field(default_factory=list)
    blocking_residuals: list[str] = field(default_factory=list)
    reason: str = ""
    runtime_authority_granted: bool = False
    provider_dispatch_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "gate_name": self.gate_name,
            "action_type": self.action_type,
            "decision": self.decision,
            "readiness_vector": self.readiness_vector,
            "missing_evidence": self.missing_evidence,
            "blocking_residuals": self.blocking_residuals,
            "reason": self.reason,
            "runtime_authority_granted": False,
            "provider_dispatch_enabled": False,
        }


def evaluate_readiness_vector(vector: dict[str, Any]) -> tuple[str, list[str]]:
    missing = [key for key, value in vector.items() if value is False or value == "Unknown" or value is None]
    if missing:
        return "BLOCKED", missing
    return "READY", []


def contains_forbidden_key(payload: Any) -> list[str]:
    found: list[str] = []
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key in FORBIDDEN_OUTPUT_FIELDS:
                found.append(key)
            found.extend(contains_forbidden_key(value))
    elif isinstance(payload, list):
        for item in payload:
            found.extend(contains_forbidden_key(item))
    return found


def refs_closed(support_refs: list[str], allowed_refs: set[str]) -> bool:
    return all(ref in allowed_refs for ref in support_refs)
