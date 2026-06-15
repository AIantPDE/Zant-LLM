from __future__ import annotations

RUNTIME_FLAGS = {
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

FORBIDDEN_OUTPUT_FIELDS = {
    "agent_action", "execution_action", "fetch_decision", "model_call",
    "provider_dispatch", "provider_registry_update", "remote_api_call",
    "route_decision", "runtime_authority", "runtime_authority_granted",
    "side_effect", "worker_trigger", "writeback_execution", "new_decision",
    "decision_override", "policy_update", "order_placement",
}

def assert_runtime_boundaries() -> None:
    leaking = [k for k, v in RUNTIME_FLAGS.items() if v is not False]
    if leaking:
        raise AssertionError(f"Runtime boundary flags must stay false: {leaking}")

def iter_keys(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield k
            yield from iter_keys(v)
    elif isinstance(obj, list):
        for item in obj:
            yield from iter_keys(item)

def forbidden_fields_in_output(output: object) -> list[str]:
    return sorted({key for key in iter_keys(output) if key in FORBIDDEN_OUTPUT_FIELDS})
