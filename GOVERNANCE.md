# Zant-LLM Governance v0.1

## Repository class

```text
EXTERNAL_MODEL_TRAINING_LINE
```

## Allowed in v0.1

```text
zant_llm_repository_created=True
zant_llm_training_started=True
zant_llm_independent_eval_allowed=True
model_card_allowed=True
release_manifest_allowed=True
checkpoint_sha256_record_allowed=True
```

## Forbidden in v0.1

```text
zant_llm_provider_connected=False
zant_model_call_enabled_in_aiant_zant=False
provider_dispatch_enabled=False
provider_registry_changed=False
route_decision_created=False
fetch_decision_created=False
runtime_loader_changed=False
worker_activation_started=False
side_effecting_execution_authorized=False
runtime_authority_granted=False
```

## Safety rule

Training code may create explanations. It may not create actions, routes, provider dispatches, fetch decisions, runtime permissions, or writeback instructions.

## Output contract

The only allowed output fields for v0.1 baseline examples are:

```text
explanation_summary
explanation_residual_hint
evidence_grounded_rationale
uncertainty_aware_wording
fail_closed_fallback
```

Any output containing a forbidden field must fail validation.
