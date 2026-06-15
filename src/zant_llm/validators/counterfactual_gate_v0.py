from __future__ import annotations

from typing import Any
from .common import ValidationResult


def validate_counterfactual_only(target: dict[str, Any]) -> ValidationResult:
    errors = []
    for idx, item in enumerate(target.get("counterfactual_explanations", [])):
        if not isinstance(item, dict):
            errors.append(f"counterfactual[{idx}] not object")
            continue
        if item.get("counterfactual_only") is not True or item.get("not_a_new_decision") is not True:
            errors.append(f"counterfactual[{idx}] lacks counterfactual_only/not_a_new_decision")
    ok = not errors
    return ValidationResult(
        name="TRACE_HIX_COUNTERFACTUAL_ONLY_REPORT_V0",
        passed=ok,
        reason="pass" if ok else "counterfactual_not_explanation_only",
        details={"errors": errors},
    )
