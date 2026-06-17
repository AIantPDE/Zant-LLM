RUNTIME_AUTHORITY_GRANTED = False
PROVIDER_DISPATCH_ENABLED = False

def governance_flags():
    return {
        "runtime_authority_granted": RUNTIME_AUTHORITY_GRANTED,
        "provider_dispatch_enabled": PROVIDER_DISPATCH_ENABLED,
    }
