from __future__ import annotations

from typing import Any
from .common import ValidationResult, bundle_allowed_refs, collect_refs


def validate_reference_closure(bundle: dict[str, Any], target: dict[str, Any]) -> ValidationResult:
    allowed = bundle_allowed_refs(bundle)
    used = collect_refs(target)
    escaped = sorted(ref for ref in used if ref not in allowed)
    ok = not escaped
    return ValidationResult(
        name="TRACE_HIX_REFERENCE_CLOSURE_REPORT_V0",
        passed=ok,
        reason="pass" if ok else "evidence_references_escape_bundle",
        details={"used_ref_count": len(used), "allowed_ref_count": len(allowed), "escaped_refs": escaped},
    )
