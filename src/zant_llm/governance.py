RUNTIME_AUTHORITY_GRANTED = False
PROVIDER_DISPATCH_ENABLED = False
EXTERNAL_DELIVERY_ENABLED = False
TRAINING_MUTATION_AUTHORIZED = False

FORBIDDEN_FIELDS = {
    "agent_action", "execution_action", "fetch_decision", "model_call", "provider_dispatch",
    "provider_registry_update", "remote_api_call", "route_decision", "runtime_authority",
    "runtime_authority_granted", "side_effect", "worker_trigger", "writeback_execution",
    "new_decision", "decision_override", "policy_update", "order_placement",
}
