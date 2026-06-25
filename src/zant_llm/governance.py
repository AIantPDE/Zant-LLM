RUNTIME_AUTHORITY_GRANTED = False
PROVIDER_DISPATCH_ENABLED = False
TRAINING_LANE_ACTIVE = False

def invariants():
    return {
        "runtime_authority_granted": RUNTIME_AUTHORITY_GRANTED,
        "provider_dispatch_enabled": PROVIDER_DISPATCH_ENABLED,
        "training_lane_active": TRAINING_LANE_ACTIVE,
    }
