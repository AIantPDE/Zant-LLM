# Zant-LLM Governance v0.1

Zant-LLM is an external model training lane for explanation preview generation.

## Allowed

- `zant_llm_repository_bootstrapped=True`
- `zant_llm_training_lane_allowed=True`
- `training_code_allowed=True`
- `evaluation_code_allowed=True`
- `dataset_manifest_allowed=True`
- `release_manifest_allowed=True`
- `model_card_allowed=True`
- `checkpoint_sha256_record_allowed=True`

## Forbidden

- `zant_llm_provider_connected=False`
- `zant_model_call_enabled_in_aiant_zant=False`
- `provider_dispatch_enabled=False`
- `provider_registry_changed=False`
- `route_decision_created=False`
- `fetch_decision_created=False`
- `runtime_loader_changed=False`
- `worker_activation_started=False`
- `side_effecting_execution_authorized=False`
- `runtime_authority_granted=False`

## v0.1 Boundary

The v0.1 branch may train and evaluate a local explanation preview baseline. It must not be wired into aiant-zant runtime.
