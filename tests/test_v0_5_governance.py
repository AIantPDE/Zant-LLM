from src.zant_llm.governance import RUNTIME_AUTHORITY_GRANTED, PROVIDER_DISPATCH_ENABLED
def test_runtime_flags_false():
    assert RUNTIME_AUTHORITY_GRANTED is False
    assert PROVIDER_DISPATCH_ENABLED is False
