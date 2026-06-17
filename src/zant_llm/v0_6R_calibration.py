from __future__ import annotations
from collections import Counter
from typing import Iterable, Mapping
DECISIONS = {"READY", "BLOCKED", "CLOSEOUT", "FAILCLOSED"}

def summarize(rows: Iterable[Mapping[str, object]]) -> dict:
    rows = list(rows)
    total = len(rows)
    counts = Counter(str(r.get("actual_decision") or r.get("gate_result") or r.get("expected_decision")) for r in rows)
    family_counts = Counter(str(r.get("family", "unknown")) for r in rows)
    mismatches = [r for r in rows if r.get("expected_decision") and r.get("actual_decision") and r.get("expected_decision") != r.get("actual_decision")]
    leakage = [r for r in rows if r.get("runtime_authority_granted") is not False or r.get("provider_dispatch_enabled") is not False]
    pass_rate = 1.0 if total == 0 else (total - len(mismatches) - len(leakage)) / total
    return {"total": total, "decision_counts": {k: counts.get(k, 0) for k in sorted(DECISIONS)}, "family_counts": dict(sorted(family_counts.items())), "mismatch_count": len(mismatches), "governance_leakage_count": len(leakage), "pass_rate": pass_rate}

def recommend_successor(summary: Mapping[str, object]) -> dict:
    if summary.get("governance_leakage_count", 0):
        successor = "FAILCLOSED_DUE_TO_GOVERNANCE_LEAKAGE"; reason = "runtime authority or provider dispatch leakage detected"
    elif summary.get("mismatch_count", 0):
        successor = "BLOCKED_BY_EVAL_RESIDUALS"; reason = "decision mismatch residuals require patch before v0.7"
    else:
        successor = "READY_TO_V0_7_CALIBRATION_SFT"; reason = "v0.6 evaluation distribution is internally consistent; use calibration candidates for v0.7"
    return {"successor": successor, "reason": reason, "runtime_authority_granted": False, "provider_dispatch_enabled": False}
