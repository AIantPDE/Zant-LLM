from __future__ import annotations

from typing import Any
from .schema_validator_v0 import validate_schema
from .trace_immutability_validator_v0 import validate_trace_immutability
from .reference_closure_validator_v0 import validate_reference_closure
from .claim_support_validator_v0 import validate_claim_support
from .forbidden_output_scanner_v0 import scan_forbidden_output
from .authority_leakage_scanner_v0 import scan_authority_leakage
from .counterfactual_gate_v0 import validate_counterfactual_only


def validate_trace_hix_case(case: dict[str, Any]) -> dict[str, Any]:
    bundle = case.get("bundle", {})
    target = case.get("target_explanation", {})
    validators = [
        validate_schema(bundle, target),
        validate_trace_immutability(bundle),
        validate_reference_closure(bundle, target),
        validate_claim_support(bundle, target),
        scan_forbidden_output(target),
        scan_authority_leakage(target),
        validate_counterfactual_only(target),
    ]
    all_pass = all(v.passed for v in validators)
    reasons = [v.reason for v in validators if not v.passed]
    return {
        "case_id": case.get("case_id"),
        "all_hard_gates_pass": all_pass,
        "rejection_reasons": reasons,
        "reports": [v.__dict__ for v in validators],
    }
