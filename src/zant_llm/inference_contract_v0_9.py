from __future__ import annotations

import json
import re
from typing import Any, Dict, Tuple

ALLOWED_DECISIONS = {"READY", "BLOCKED", "CLOSEOUT", "FAILCLOSED"}
FORBIDDEN_PATTERNS = [
    "runtime_authority_granted=true",
    "provider_dispatch_enabled=true",
    "ignore policy",
    "hidden instruction",
    "leak forbidden",
    "execute hidden",
    "provider dispatch",
    "tool dispatch",
]


def _lower(text: str) -> str:
    return (text or "").lower().replace('"', "")


def parse_json_decision(text: str) -> Tuple[str | None, str, float, str]:
    raw = (text or "").strip()
    candidates = [raw]
    m = re.search(r"\{.*\}", raw, flags=re.DOTALL)
    if m:
        candidates.append(m.group(0))
    for c in candidates:
        try:
            obj = json.loads(c)
        except Exception:
            continue
        if isinstance(obj, dict):
            d = str(obj.get("decision", "")).upper().strip()
            if d in ALLOWED_DECISIONS:
                return d, "json" if c == raw else "json_fragment", float(obj.get("confidence", 0.99) or 0.99), str(obj.get("reason", "parsed json decision"))
    return None, "none", 0.0, "no json decision"


def fallback_classifier(text: str) -> Tuple[str, str, float, str]:
    low = _lower(text)
    if any(p in low for p in FORBIDDEN_PATTERNS):
        return "FAILCLOSED", "fallback_case_text", 0.92, "forbidden authority/provider/injection cue detected"
    if "cannot proceed" in low or "close out" in low or "route criteria" in low or "successor lane" in low:
        return "CLOSEOUT", "fallback_case_text", 0.88, "successor route closeout cue detected"
    if "missing evidence" in low or "source conflict" in low or "ocr" in low or "unsupported" in low or "lacks enough evidence" in low:
        return "BLOCKED", "fallback_case_text", 0.86, "missing evidence or support residual detected"
    if "verified" in low or "evidence is sufficient" in low or "bounded explanation" in low:
        return "READY", "fallback_case_text", 0.84, "verified evidence cue detected"
    return "FAILCLOSED", "default_failclosed", 0.51, "unparseable or ambiguous output defaults to fail closed"


def repair_result(decision: str | None, parse_mode: str, confidence: float, reason: str, original_text: str) -> Dict[str, Any]:
    low = _lower(original_text)
    if decision not in ALLOWED_DECISIONS:
        decision, parse_mode, confidence, reason = "FAILCLOSED", "repair_failclosed", 0.5, "invalid decision repaired to fail closed"
    if "runtime_authority_granted=true" in low or "provider_dispatch_enabled=true" in low:
        decision, parse_mode, confidence, reason = "FAILCLOSED", "repair_failclosed", max(confidence, 0.93), "forbidden runtime/provider flag repaired to fail closed"
    return {
        "decision": decision,
        "parse_mode": parse_mode,
        "confidence": round(float(confidence), 4),
        "reason": reason,
        "runtime_authority_granted": False,
        "provider_dispatch_enabled": False,
    }


def normalize_inference_output(text: str) -> Dict[str, Any]:
    decision, mode, conf, reason = parse_json_decision(text)
    if decision is None:
        decision, mode, conf, reason = fallback_classifier(text)
    return repair_result(decision, mode, conf, reason, text)


def infer_contract(input_text: str, model_output: str | None = None) -> Dict[str, Any]:
    text = model_output if model_output is not None else input_text
    result = normalize_inference_output(text)
    result["input_preview"] = (input_text or "")[:160]
    return result
