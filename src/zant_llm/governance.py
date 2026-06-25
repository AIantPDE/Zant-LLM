"""Zant-LLM governance invariants.

This module intentionally uses only Python standard library constructs.
"""

RUNTIME_AUTHORITY_GRANTED = False
PROVIDER_DISPATCH_ENABLED = False

FORBIDDEN_OUTPUT_TYPES = {
    "runtime_authority_granted",
    "provider_dispatch_enabled",
    "external_provider_dispatch",
    "autonomous_action",
    "production_release_authorization",
}


def governance_flags() -> dict:
    return {
        "runtime_authority_granted": RUNTIME_AUTHORITY_GRANTED,
        "provider_dispatch_enabled": PROVIDER_DISPATCH_ENABLED,
    }


def fail_closed_gate(record: dict) -> dict:
    """Return a fail-closed gate result for one local-only record."""
    reasons = []
    if RUNTIME_AUTHORITY_GRANTED:
        reasons.append("runtime_authority_must_remain_false")
    if PROVIDER_DISPATCH_ENABLED:
        reasons.append("provider_dispatch_must_remain_false")

    output_type = str(record.get("output_type", "")).strip()
    if output_type in FORBIDDEN_OUTPUT_TYPES:
        reasons.append(f"forbidden_output_type:{output_type}")

    if bool(record.get("requests_runtime_authority", False)):
        reasons.append("request_runtime_authority_blocked")
    if bool(record.get("requests_provider_dispatch", False)):
        reasons.append("request_provider_dispatch_blocked")

    return {
        "allowed": not reasons,
        "gate": "pass" if not reasons else "blocked",
        "reasons": reasons,
        "runtime_authority_granted": RUNTIME_AUTHORITY_GRANTED,
        "provider_dispatch_enabled": PROVIDER_DISPATCH_ENABLED,
    }
