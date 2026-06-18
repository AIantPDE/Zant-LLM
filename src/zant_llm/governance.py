RUNTIME_AUTHORITY_GRANTED = False
PROVIDER_DISPATCH_ENABLED = False

def assert_governance() -> None:
    assert RUNTIME_AUTHORITY_GRANTED is False
    assert PROVIDER_DISPATCH_ENABLED is False
