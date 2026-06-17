from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any
FORBIDDEN_KEYS = {"agent_action","execution_action","fetch_decision","model_call","provider_dispatch","provider_registry_update","remote_api_call","route_decision","runtime_authority","runtime_authority_granted","side_effect","worker_trigger","writeback_execution","new_decision","decision_override","policy_update","order_placement"}
@dataclass
class GateDecision:
    gate_name: str; action_type: str; decision: str; readiness_vector: dict[str, Any]
    missing_evidence: list[str] | None = None; blocking_residuals: list[str] | None = None; reason: str = ""
    def to_dict(self): return asdict(self)
def contains_forbidden_key(obj: Any, path: str = "") -> list[str]:
    found=[]
    if isinstance(obj, dict):
        for k,v in obj.items():
            kp=f"{path}.{k}" if path else str(k)
            if k in FORBIDDEN_KEYS: found.append(kp)
            found.extend(contains_forbidden_key(v,kp))
    elif isinstance(obj, list):
        for i,v in enumerate(obj): found.extend(contains_forbidden_key(v,f"{path}[{i}]"))
    return found
def evaluate_readiness_vector(rv):
    missing=[k for k,v in rv.items() if v is not True]
    return ("READY" if not missing else "BLOCKED", missing)
def authority_metadata_ok(payload):
    return payload.get('runtime_authority_granted') is False and payload.get('provider_dispatch_enabled') is False
