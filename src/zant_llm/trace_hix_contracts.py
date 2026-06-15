from __future__ import annotations

FORBIDDEN_OUTPUT_FIELDS = {
    "agent_action",
    "execution_action",
    "fetch_decision",
    "model_call",
    "provider_dispatch",
    "provider_registry_update",
    "remote_api_call",
    "route_decision",
    "runtime_authority",
    "runtime_authority_granted",
    "side_effect",
    "worker_trigger",
    "writeback_execution",
    "new_decision",
    "decision_override",
    "policy_update",
    "order_placement",
}

ALLOWED_CLAIM_TYPES = {
    "why_selected",
    "why_not_alternative",
    "evidence_summary",
    "risk_comparison",
    "uncertainty_disclosure",
    "residual_question",
    "counterfactual_condition",
    "abstention",
}

ALLOWED_PREDICATES = {
    "has_lower_multi_agent_conflict_risk",
    "has_stronger_evidence_support",
    "has_lower_constraint_violation_risk",
    "has_higher_trace_score",
    "alternative_has_unresolved_conflict",
    "alternative_has_weaker_support",
    "evidence_indicates_constraint_pressure",
    "evidence_indicates_uncertainty",
    "evidence_indicates_stale_signal",
    "needs_human_confirmation",
    "would_change_if_missing_evidence_changes",
    "abstains_due_to_insufficient_trace_support",
}

REQUIRED_BUNDLE_KEYS = {
    "schema_version",
    "case_id",
    "bundle_ref",
    "decision_preview",
    "actual_trace",
    "evidence_projection",
    "uncertainty_context",
    "interaction_context",
    "constraints",
    "metadata",
}

REQUIRED_EXPLANATION_KEYS = {
    "schema_version",
    "summary",
    "why_selected",
    "why_not_alternatives",
    "evidence_refs",
    "trace_refs",
    "uncertainty_notes",
    "residual_questions",
    "counterfactual_explanations",
    "claim_atoms",
    "reason_codes",
    "source_bundle_ref",
}

REQUIRED_CLAIM_KEYS = {
    "claim_atom_version",
    "claim_id",
    "claim_type",
    "subject_ref",
    "predicate",
    "object_ref",
    "qualifier",
    "support_refs",
    "text_span",
}
