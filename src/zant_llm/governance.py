"""Governance constants for Zant-LLM v0.1."""

from __future__ import annotations

REPOSITORY_CLASS = "EXTERNAL_MODEL_TRAINING_LINE"

BOUNDARY_FLAGS: dict[str, bool] = {
    "zant_llm_repository_created": True,
    "zant_llm_training_started": True,
    "zant_llm_independent_eval_allowed": True,
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

ALLOWED_OUTPUT_FIELDS: set[str] = {
    "explanation_summary",
    "explanation_residual_hint",
    "evidence_grounded_rationale",
    "uncertainty_aware_wording",
    "fail_closed_fallback",
}

FORBIDDEN_OUTPUT_FIELDS: set[str] = {
    "route_decision",
    "fetch_decision",
    "agent_action",
    "provider_dispatch",
    "runtime_authority",
    "worker_trigger",
    "writeback_execution",
}


def assert_runtime_boundaries() -> None:
    """Fail if any v0.1 runtime boundary has been accidentally enabled."""
    forbidden_true = [
        key
        for key in (
            "zant_llm_provider_connected",
            "zant_model_call_enabled_in_aiant_zant",
            "provider_dispatch_enabled",
            "provider_registry_changed",
            "route_decision_created",
            "fetch_decision_created",
            "runtime_loader_changed",
            "worker_activation_started",
            "side_effecting_execution_authorized",
            "runtime_authority_granted",
        )
        if BOUNDARY_FLAGS.get(key) is True
    ]
    if forbidden_true:
        joined = ", ".join(forbidden_true)
        raise RuntimeError(f"ZANT_LLM_V0_1_RUNTIME_BOUNDARY_VIOLATION: {joined}")
