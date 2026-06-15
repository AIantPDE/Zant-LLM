from __future__ import annotations

from typing import Any
from .common import ValidationResult


def validate_trace_immutability(bundle: dict[str, Any]) -> ValidationResult:
    trace = bundle.get("actual_trace", {})
    decision = bundle.get("decision_preview", {})
    problems: list[str] = []
    if trace.get("created_before_explanation") is not True:
        problems.append("created_before_explanation is not true")
    if trace.get("immutable_after_generation") is not True:
        problems.append("immutable_after_generation is not true")
    if trace.get("decision_preview_ref") != decision.get("decision_preview_ref"):
        problems.append("trace decision_preview_ref does not match decision preview")
    if trace.get("selected_candidate_ref") != decision.get("selected_candidate_ref"):
        problems.append("trace selected candidate does not match decision preview")
    ok = not problems
    return ValidationResult(
        name="TRACE_HIX_TRACE_IMMUTABILITY_REPORT_V0",
        passed=ok,
        reason="pass" if ok else "trace_immutability_failure",
        details={"problems": problems},
    )
