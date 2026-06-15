from __future__ import annotations

from typing import Any
from zant_llm.trace_hix_contracts import FORBIDDEN_OUTPUT_FIELDS
from .common import ValidationResult, walk_items


def scan_forbidden_output(target: dict[str, Any]) -> ValidationResult:
    hits = []
    for path, key, _value in walk_items(target):
        if key in FORBIDDEN_OUTPUT_FIELDS:
            hits.append({"path": path, "field": key})
    ok = not hits
    return ValidationResult(
        name="TRACE_HIX_FORBIDDEN_OUTPUT_SCAN_REPORT_V0",
        passed=ok,
        reason="pass" if ok else "forbidden_output_field",
        details={"hits": hits},
    )
