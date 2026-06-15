ALLOWED = {"has_lower_multi_agent_conflict_risk", "alternative_has_higher_constraint_risk", "has_bounded_uncertainty", "requires_human_confirmation", "counterfactual_only_condition", "abstains_due_to_missing_evidence", "summarizes_evidence_ref"}

def validate_claim_support(bundle: dict, explanation: dict) -> dict:
    refs = set(bundle.get("actual_trace", {}).get("input_evidence_refs", []))
    refs.add(bundle.get("decision_preview", {}).get("selected_candidate_ref", ""))
    refs.update(bundle.get("decision_preview", {}).get("alternative_candidate_refs", []))
    errors = []
    for atom in explanation.get("claim_atoms", []):
        support = set(atom.get("support_refs", []))
        if atom.get("predicate") not in ALLOWED:
            errors.append({"claim_id": atom.get("claim_id"), "error":"predicate_not_allowed"})
        if not support or not support.issubset(refs):
            errors.append({"claim_id": atom.get("claim_id"), "error":"support_refs_invalid"})
    return {"validator":"ClaimSupportValidatorV0", "passed": not errors, "errors": errors}
