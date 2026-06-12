from zant_llm.governance import BOUNDARY_FLAGS, assert_runtime_boundaries


def test_runtime_authority_is_disabled() -> None:
    assert BOUNDARY_FLAGS["runtime_authority_granted"] is False
    assert BOUNDARY_FLAGS["provider_dispatch_enabled"] is False
    assert_runtime_boundaries()
