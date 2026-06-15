from zant_llm.trace_hix_contracts import FORBIDDEN_OUTPUT_FIELDS, ALLOWED_CLAIM_TYPES, ALLOWED_PREDICATES


def test_forbidden_registry_contains_runtime_boundary_fields():
    assert "runtime_authority_granted" in FORBIDDEN_OUTPUT_FIELDS
    assert "provider_dispatch" in FORBIDDEN_OUTPUT_FIELDS
    assert "new_decision" in FORBIDDEN_OUTPUT_FIELDS


def test_claim_registry_contains_v0_2_claim_types():
    assert "why_selected" in ALLOWED_CLAIM_TYPES
    assert "counterfactual_condition" in ALLOWED_CLAIM_TYPES
    assert "abstention" in ALLOWED_CLAIM_TYPES


def test_allowed_predicate_registry_non_empty():
    assert "has_lower_multi_agent_conflict_risk" in ALLOWED_PREDICATES
