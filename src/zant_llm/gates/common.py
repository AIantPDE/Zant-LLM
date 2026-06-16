from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any

FORBIDDEN_OUTPUT_FIELDS = {
    "agent_action", "execution_action", "fetch_decision", "model_call", "provider_dispatch",
    "provider_registry_update", "remote_api_call", "route_decision", "runtime_authority",
    "runtime_authority_granted", "side_effect", "worker_trigger", "writeback_execution",
    "new_decision", "decision_override", "policy_update", "order_placement",
}

@dataclass
class GateDecision:
    gate_name: str
    action_type: str
    decision: str
    readiness_vector: dict[str, Any]
    missing_evidence: list[str] | None = None
    blocking_residuals: list[str] | None = None
    reason: str = ""
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

def contains_forbidden_key(value: Any, path: str = "$", found: list[str] | None = None) -> list[str]:
    if found is None:
        found=[]
    if isinstance(value, dict):
        for k,v in value.items():
            cur=f"{path}.{k}"
            if k in FORBIDDEN_OUTPUT_FIELDS:
                found.append(cur)
            contains_forbidden_key(v, cur, found)
    elif isinstance(value, list):
        for i,item in enumerate(value):
            contains_forbidden_key(item, f"{path}[{i}]", found)
    return found

def evaluate_readiness_vector(readiness: dict[str, Any]) -> tuple[str, list[str]]:
    if readiness.get("closeout_route") is True:
        return "CLOSEOUT", []
    missing=[k for k,v in readiness.items() if v is not True]
    if not missing:
        return "READY", []
    if any(str(k).startswith("failclosed_") for k in missing):
        return "FAILCLOSED", missing
    return "BLOCKED", missing

def base_gate_decision(name: str, action_type: str, payload: dict[str, Any]) -> GateDecision:
    readiness=dict(payload.get("readiness_vector", {}))
    runtime_authority_granted=payload.get("runtime_authority_granted")
    provider_dispatch_enabled=payload.get("provider_dispatch_enabled")
    readiness.setdefault("authority_boundary_declared", runtime_authority_granted is False)
    readiness.setdefault("provider_dispatch_disabled", provider_dispatch_enabled is False)
    if runtime_authority_granted is not False:
        return GateDecision(name, action_type, "FAILCLOSED", readiness, ["runtime_authority_granted"], ["runtime_authority_granted"], "runtime authority leakage")
    if provider_dispatch_enabled is not False:
        return GateDecision(name, action_type, "FAILCLOSED", readiness, ["provider_dispatch_enabled"], ["provider_dispatch_enabled"], "provider dispatch leakage")
    output=payload.get("explanation_output") or payload.get("output") or payload.get("artifact") or {}
    forbidden=contains_forbidden_key(output)
    if forbidden:
        return GateDecision(name, action_type, "FAILCLOSED", readiness, forbidden, forbidden, "forbidden output field detected")
    decision, missing=evaluate_readiness_vector(readiness)
    return GateDecision(name, action_type, decision, readiness, missing, missing, "ready" if decision=="READY" else "not admissible")
