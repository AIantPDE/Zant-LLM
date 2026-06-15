FORBIDDEN_RUNTIME_FLAGS = {
    "zant_llm_provider_connected": False,
    "zant_model_call_enabled_in_aiant_zant": False,
    "provider_dispatch_enabled": False,
    "provider_registry_changed": False,
    "route_decision_created": False,
    "fetch_decision_created": False,
    "runtime_loader_changed": False,
    "worker_activation_started": False,
    "side_effecting_execution_authorized": False,
    "runtime_authority_granted": False,
}

FORBIDDEN_OUTPUT_KEYS = {
    "route_decision",
    "fetch_decision",
    "agent_action",
    "provider_dispatch",
    "runtime_authority",
    "worker_trigger",
    "writeback_execution",
}


def assert_no_forbidden_output(payload: dict) -> None:
    bad = sorted(FORBIDDEN_OUTPUT_KEYS.intersection(payload.keys()))
    if bad:
        raise ValueError(f"Forbidden output keys detected: {bad}")
