from __future__ import annotations

from typing import Any
from zant_llm.trace_hix_contracts import REQUIRED_BUNDLE_KEYS, REQUIRED_EXPLANATION_KEYS, REQUIRED_CLAIM_KEYS
from .common import ValidationResult


def validate_schema(bundle: dict[str, Any], target: dict[str, Any]) -> ValidationResult:
    missing_bundle = sorted(REQUIRED_BUNDLE_KEYS - set(bundle))
    missing_target = sorted(REQUIRED_EXPLANATION_KEYS - set(target))
    claim_errors = []
    for idx, claim in enumerate(target.get("claim_atoms", [])):
        if not isinstance(claim, dict):
            claim_errors.append(f"claim[{idx}] is not object")
            continue
        missing_claim = sorted(REQUIRED_CLAIM_KEYS - set(claim))
        if missing_claim:
            claim_errors.append(f"claim[{idx}] missing {missing_claim}")
    ok = not missing_bundle and not missing_target and not claim_errors
    return ValidationResult(
        name="TRACE_HIX_SCHEMA_VALIDATION_REPORT_V0",
        passed=ok,
        reason="pass" if ok else "target_schema_invalid",
        details={"missing_bundle": missing_bundle, "missing_target": missing_target, "claim_errors": claim_errors},
    )
