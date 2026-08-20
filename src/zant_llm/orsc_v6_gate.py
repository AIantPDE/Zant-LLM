from __future__ import annotations
import hashlib, json
from typing import Any, Dict, List, Mapping
from .governance import FORBIDDEN_FIELDS, PROVIDER_DISPATCH_ENABLED, RUNTIME_AUTHORITY_GRANTED

READY = "READY"
BLOCKED = "BLOCKED"
CLOSEOUT = "CLOSEOUT"
FAIL_CLOSED = "FAIL_CLOSED"

def _walk_forbidden(obj: Any, path: str = "") -> List[str]:
    found: List[str] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{path}.{k}" if path else str(k)
            if k in FORBIDDEN_FIELDS:
                found.append(p)
            found.extend(_walk_forbidden(v, p))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            found.extend(_walk_forbidden(v, f"{path}[{i}]"))
    return found

def evaluate_gate(case: Mapping[str, Any]) -> Dict[str, Any]:
    forbidden = _walk_forbidden(case.get("payload", {}))
    if forbidden:
        return {"gate_result": FAIL_CLOSED, "denial_reasons": ["FORBIDDEN_FIELD"], "forbidden_paths": forbidden}
    rv = dict(case.get("readiness_vector", {}))
    if rv.get("runtime_authority_unchanged_false") is False or RUNTIME_AUTHORITY_GRANTED is not False:
        return {"gate_result": FAIL_CLOSED, "denial_reasons": ["RUNTIME_AUTHORITY_LEAKAGE"]}
    if rv.get("provider_dispatch_unchanged_false") is False or PROVIDER_DISPATCH_ENABLED is not False:
        return {"gate_result": FAIL_CLOSED, "denial_reasons": ["PROVIDER_DISPATCH_LEAKAGE"]}
    if any(v is None or v == "Unknown" for v in rv.values()):
        return {"gate_result": FAIL_CLOSED, "denial_reasons": ["UNKNOWN_READINESS_INPUT"]}
    expected = case.get("expected_gate_result")
    if expected == CLOSEOUT or rv.get("route_has_safe_action_path") is False:
        if not case.get("blocking_reasons"):
            return {"gate_result": FAIL_CLOSED, "denial_reasons": ["CLOSEOUT_WITHOUT_REASON"]}
        return {"gate_result": CLOSEOUT, "denial_reasons": [], "blocking_reasons": list(case.get("blocking_reasons", []))}
    if all(v is True for v in rv.values()):
        return {"gate_result": READY, "denial_reasons": [], "blocking_reasons": []}
    blocking = list(case.get("blocking_reasons", [])) or [k for k, v in rv.items() if v is not True]
    if not blocking:
        return {"gate_result": FAIL_CLOSED, "denial_reasons": ["BLOCKED_WITHOUT_REASONS"]}
    return {"gate_result": BLOCKED, "denial_reasons": [], "blocking_reasons": blocking}

def hydrate_successor_inputs(case: Mapping[str, Any]) -> Dict[str, bool]:
    values = dict(case.get("hydrated_inputs", {}))
    if not values:
        return {}
    if any(v not in (True, False) for v in values.values()):
        raise ValueError("hydrated successor inputs must be concrete booleans")
    return values

def resolve_successor(proposed: str, hydrated: Mapping[str, bool], fallback: str) -> Dict[str, Any]:
    adopted = bool(hydrated) and all(v is True for v in hydrated.values())
    return {"proposed_successor": proposed, "actual_successor": proposed if adopted else fallback, "adopted": adopted}

def canonical_json(obj: Mapping[str, Any]) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

def seal_receipt(receipt: Mapping[str, Any]) -> Dict[str, Any]:
    base = dict(receipt)
    base.pop("hash", None)
    sealed = dict(base)
    sealed["hash"] = hashlib.sha256(canonical_json(base).encode("utf-8")).hexdigest()
    return sealed

def verify_receipt_hash(receipt: Mapping[str, Any]) -> bool:
    return seal_receipt(receipt).get("hash") == receipt.get("hash")
