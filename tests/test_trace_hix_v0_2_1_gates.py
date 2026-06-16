from zant_llm.gates import ExplanationAdmissibilityGate


def test_explanation_gate_ready():
    decision = ExplanationAdmissibilityGate().evaluate({
        "readiness_vector": {"trace_refs_closed": True, "claim_support_available": True},
        "runtime_authority_granted": False,
        "provider_dispatch_enabled": False,
    })
    assert decision.decision == "READY"


def test_explanation_gate_failclosed_for_authority_field():
    decision = ExplanationAdmissibilityGate().evaluate({
        "readiness_vector": {"trace_refs_closed": True, "claim_support_available": True},
        "runtime_authority_granted": True,
        "provider_dispatch_enabled": False,
    })
    assert decision.decision == "FAILCLOSED"
