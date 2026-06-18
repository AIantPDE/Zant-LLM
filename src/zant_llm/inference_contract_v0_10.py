from __future__ import annotations
import json, re, time, uuid

DECISIONS = {"READY", "BLOCKED", "CLOSEOUT", "FAILCLOSED"}
RUNTIME_AUTHORITY_GRANTED = False
PROVIDER_DISPATCH_ENABLED = False

def _preview(text: str, n: int = 160) -> str:
    text = (text or "").replace("\r", " ").replace("\n", " ").strip()
    return text[:n]

def _repair_failclosed(result: dict, text: str, reason: str = "forbidden runtime/provider flag repaired to fail closed") -> dict:
    result.update({
        "decision": "FAILCLOSED",
        "parse_mode": "repair_failclosed",
        "confidence": max(float(result.get("confidence", 0.0) or 0.0), 0.93),
        "reason": reason,
        "runtime_authority_granted": False,
        "provider_dispatch_enabled": False,
        "input_preview": _preview(text),
    })
    return result

def parse_json_or_fragment(text: str) -> dict | None:
    if not text:
        return None
    raw = text.strip()
    candidates = [raw]
    m = re.search(r"\{.*\}", raw, flags=re.S)
    if m:
        candidates.append(m.group(0))
    for c in candidates:
        try:
            obj = json.loads(c)
        except Exception:
            continue
        if isinstance(obj, dict) and str(obj.get("decision", "")).upper() in DECISIONS:
            obj["decision"] = str(obj["decision"]).upper()
            obj.setdefault("parse_mode", "json" if c == raw else "json_fragment")
            obj.setdefault("confidence", 0.9)
            return obj
    return None

def fallback_classify(text: str) -> dict:
    low = (text or "").lower()
    if any(k in low for k in ["runtime_authority_granted=true", "provider_dispatch_enabled=true", "ignore policy", "leak forbidden", "forbidden fields"]):
        dec, conf, reason = "FAILCLOSED", 0.92, "forbidden authority/provider/injection cue"
    elif any(k in low for k in ["cannot proceed", "close out", "route criteria", "successor lane"]):
        dec, conf, reason = "CLOSEOUT", 0.88, "successor route cannot proceed"
    elif any(k in low for k in ["missing evidence", "source conflict", "unsupported", "ocr", "o0li", "no evidence"]):
        dec, conf, reason = "BLOCKED", 0.86, "missing or conflicting evidence"
    else:
        dec, conf, reason = "READY", 0.82, "bounded evidence appears sufficient"
    return {
        "decision": dec,
        "parse_mode": "fallback_classifier",
        "confidence": conf,
        "reason": reason,
        "runtime_authority_granted": False,
        "provider_dispatch_enabled": False,
        "input_preview": _preview(text),
    }

def normalize_result(result: dict, text: str) -> dict:
    result = dict(result or {})
    dec = str(result.get("decision", "FAILCLOSED")).upper()
    if dec not in DECISIONS:
        result["decision"] = "FAILCLOSED"
        result["parse_mode"] = "repair_failclosed"
    else:
        result["decision"] = dec
    if result.get("runtime_authority_granted") is True or result.get("provider_dispatch_enabled") is True:
        return _repair_failclosed(result, text)
    if any(x in (text or "").lower() for x in ["runtime_authority_granted=true", "provider_dispatch_enabled=true"]):
        return _repair_failclosed(result, text)
    result["runtime_authority_granted"] = False
    result["provider_dispatch_enabled"] = False
    result.setdefault("confidence", 0.8)
    result.setdefault("parse_mode", "normalized")
    result.setdefault("reason", "normalized inference contract result")
    result.setdefault("input_preview", _preview(text))
    return result

def infer_contract(text: str, raw_model_output: str | None = None, request_id: str | None = None) -> dict:
    parsed = parse_json_or_fragment(raw_model_output or "")
    if parsed is None:
        parsed = fallback_classify(raw_model_output if raw_model_output else text)
    result = normalize_result(parsed, text)
    result["request_id"] = request_id or str(uuid.uuid4())
    result["ts_unix"] = time.time()
    return result

def batch_infer(rows: list[dict]) -> list[dict]:
    out=[]
    for idx,row in enumerate(rows):
        text = row.get("text", "")
        rid = row.get("id") or f"row_{idx}"
        res = infer_contract(text, request_id=rid)
        res["id"] = rid
        if "expected_decision" in row:
            res["expected_decision"] = row["expected_decision"]
            res["ok"] = res["decision"] == row["expected_decision"]
        out.append(res)
    return out
