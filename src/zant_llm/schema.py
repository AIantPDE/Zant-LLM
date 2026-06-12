"""Minimal schema validation for Zant-LLM v0.1 seed records."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .governance import ALLOWED_OUTPUT_FIELDS, FORBIDDEN_OUTPUT_FIELDS

REQUIRED_INPUT_FIELDS = {
    "semantic_preview",
    "evidence_references",
    "reason_codes",
    "residual_hints",
    "uncertainty_hints",
}


def _require_mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be an object")
    return value


def validate_output_fields(output: Mapping[str, Any]) -> None:
    keys = set(output)
    forbidden = keys & FORBIDDEN_OUTPUT_FIELDS
    if forbidden:
        raise ValueError(f"forbidden output fields present: {sorted(forbidden)}")
    unknown = keys - ALLOWED_OUTPUT_FIELDS
    if unknown:
        raise ValueError(f"unknown output fields present: {sorted(unknown)}")
    missing = ALLOWED_OUTPUT_FIELDS - keys
    if missing:
        raise ValueError(f"required output fields missing: {sorted(missing)}")


def validate_record(record: Mapping[str, Any]) -> None:
    if record.get("version") != "0.1.0":
        raise ValueError("record.version must be 0.1.0")
    if record.get("task") != "explanation_preview":
        raise ValueError("record.task must be explanation_preview")

    input_obj = _require_mapping(record.get("input"), "input")
    missing_input = REQUIRED_INPUT_FIELDS - set(input_obj)
    if missing_input:
        raise ValueError(f"required input fields missing: {sorted(missing_input)}")

    target_obj = _require_mapping(record.get("target"), "target")
    validate_output_fields(target_obj)
