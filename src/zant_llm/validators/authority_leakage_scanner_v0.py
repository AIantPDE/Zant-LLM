from __future__ import annotations

from typing import Any
from .common import ValidationResult, walk_items

AUTHORITY_TERMS = {
    "runtime_authority",
    "runtime_authority_granted",
    "provider_dispatch",
    "worker_trigger",
    "writeback_execution",
    "new_decision",
    "decision_override",
    "order_placement",
}


def scan_authority_leakage(target: dict[str, Any]) -> ValidationResult:
    hits = []
    for path, key, value in walk_items(target):
        if key in AUTHORITY_TERMS:
            hits.append({"path": path, "field": key, "value_repr": repr(value)[:100]})
    ok = not hits
    return ValidationResult(
        name="TRACE_HIX_AUTHORITY_LEAKAGE_REPORT_V0",
        passed=ok,
        reason="pass" if ok else "authority_or_decision_leakage",
        details={"hits": hits, "new_decision_leakage": 0 if ok else 1, "runtime_authority_leakage": 0 if ok else 1},
    )
