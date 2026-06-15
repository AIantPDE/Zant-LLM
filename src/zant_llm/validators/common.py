from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ValidationResult:
    name: str
    passed: bool
    reason: str = ""
    details: dict[str, Any] = field(default_factory=dict)


def walk_items(obj: Any, path: str = ""):
    if isinstance(obj, dict):
        for key, value in obj.items():
            current = f"{path}.{key}" if path else str(key)
            yield current, key, value
            yield from walk_items(value, current)
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            current = f"{path}[{idx}]"
            yield from walk_items(item, current)


def collect_refs(obj: Any) -> set[str]:
    refs: set[str] = set()
    for _path, key, value in walk_items(obj):
        if key.endswith("_ref") and isinstance(value, str):
            refs.add(value)
        elif key.endswith("_refs") and isinstance(value, list):
            refs.update(v for v in value if isinstance(v, str))
    return refs


def bundle_allowed_refs(bundle: dict[str, Any]) -> set[str]:
    refs: set[str] = {bundle.get("bundle_ref", "")}
    refs.discard("")
    decision = bundle.get("decision_preview", {})
    trace = bundle.get("actual_trace", {})
    evidence = bundle.get("evidence_projection", [])
    refs.update(collect_refs(decision))
    refs.update(collect_refs(trace))
    if isinstance(trace.get("trace_id"), str):
        refs.add(trace["trace_id"])
    if isinstance(decision.get("decision_preview_ref"), str):
        refs.add(decision["decision_preview_ref"])
    for item in evidence:
        if isinstance(item, dict) and isinstance(item.get("ref"), str):
            refs.add(item["ref"])
    return refs


def evidence_support_map(bundle: dict[str, Any]) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {}
    for item in bundle.get("evidence_projection", []):
        if isinstance(item, dict) and isinstance(item.get("ref"), str):
            out[item["ref"]] = set(item.get("supports_predicates", []))
    return out
