from zant_llm.governance import FORBIDDEN_RUNTIME_FLAGS, assert_no_forbidden_output


def test_runtime_flags_are_false():
    assert FORBIDDEN_RUNTIME_FLAGS["runtime_authority_granted"] is False
    assert FORBIDDEN_RUNTIME_FLAGS["provider_dispatch_enabled"] is False


def test_forbidden_output_detection():
    try:
        assert_no_forbidden_output({"route_decision": "allow"})
    except ValueError:
        return
    raise AssertionError("expected forbidden output detection")
