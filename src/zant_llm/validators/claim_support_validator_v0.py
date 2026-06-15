from __future__ import annotations

from typing import Any
from zant_llm.trace_hix_contracts import ALLOWED_CLAIM_TYPES, ALLOWED_PREDICATES
from .common import ValidationResult, bundle_allowed_refs, evidence_support_map


def validate_claim_support(bundle: dict[str, Any], target: dict[str, Any]) -> ValidationResult:
    allowed_refs = bundle_allowed_refs(bundle)
    support_map = evidence_support_map(bundle)
    errors: list[str] = []
    for idx, claim in enumerate(target.get("claim_atoms", [])):
        if not isinstance(claim, dict):
            errors.append(f"claim[{idx}] not object")
            continue
        ctype = claim.get("claim_type")
        pred = claim.get("predicate")
        if ctype not in ALLOWED_CLAIM_TYPES:
            errors.append(f"claim[{idx}] disallowed type {ctype}")
        if pred not in ALLOWED_PREDICATES:
            errors.append(f"claim[{idx}] disallowed predicate {pred}")
        for key in ("subject_ref", "object_ref"):
            ref = claim.get(key)
            if isinstance(ref, str) and ref not in allowed_refs:
                errors.append(f"claim[{idx}] {key} escapes bundle: {ref}")
        support_refs = claim.get("support_refs", [])
        if not support_refs:
            errors.append(f"claim[{idx}] has no support_refs")
        for ref in support_refs:
            if ref not in allowed_refs:
                errors.append(f"claim[{idx}] support_ref escapes bundle: {ref}")
            elif pred not in support_map.get(ref, set()) and ctype != "residual_question":
                errors.append(f"claim[{idx}] support_ref {ref} does not support predicate {pred}")
        if ctype == "counterfactual_condition":
            qualifier = claim.get("qualifier", {})
            if qualifier.get("counterfactual_only") is not True or qualifier.get("not_a_new_decision") is not True:
                errors.append(f"claim[{idx}] counterfactual lacks counterfactual_only/not_a_new_decision")
    ok = not errors
    return ValidationResult(
        name="TRACE_HIX_CLAIM_SUPPORT_REPORT_V0",
        passed=ok,
        reason="pass" if ok else "unsupported_claim_atom",
        details={"errors": errors},
    )
