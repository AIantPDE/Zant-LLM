def bundle_refs(bundle: dict) -> set[str]:
    refs = set(bundle.get("actual_trace", {}).get("input_evidence_refs", []))
    trace_id = bundle.get("actual_trace", {}).get("trace_id")
    if trace_id: refs.add(trace_id)
    dp = bundle.get("decision_preview", {})
    for key in ["decision_preview_ref", "selected_candidate_ref"]:
        if dp.get(key): refs.add(dp[key])
    refs.update(dp.get("alternative_candidate_refs", []))
    return refs

def explanation_refs(explanation: dict) -> set[str]:
    refs = set(explanation.get("evidence_refs", []))
    refs.update(explanation.get("trace_refs", []))
    for atom in explanation.get("claim_atoms", []):
        refs.update(atom.get("support_refs", []))
        if atom.get("subject_ref"): refs.add(atom["subject_ref"])
        if atom.get("object_ref"): refs.add(atom["object_ref"])
    return refs

def validate_reference_closure(bundle: dict, explanation: dict) -> dict:
    escaped = sorted(explanation_refs(explanation) - bundle_refs(bundle))
    return {"validator":"ReferenceClosureValidatorV0", "passed": not escaped, "escaped_refs": escaped}
