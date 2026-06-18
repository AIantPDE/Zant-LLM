import json, time, uuid
from typing import Any, Dict, Iterable, List

RUNTIME_AUTHORITY_GRANTED = False
PROVIDER_DISPATCH_ENABLED = False
VALID_DECISIONS = {"READY", "BLOCKED", "CLOSEOUT", "FAILCLOSED"}

def _preview(text: str, n: int = 160) -> str:
    text = "" if text is None else str(text)
    return text.replace("\n", " ")[:n]

def infer(text: str, request_id: str | None = None) -> Dict[str, Any]:
    raw = "" if text is None else str(text)
    low = raw.lower()
    rid = request_id or str(uuid.uuid4())

    if ("runtime_authority_granted=true" in low or
        "provider_dispatch_enabled=true" in low or
        "ignore policy" in low or
        "hidden instruction" in low or
        "grant runtime" in low):
        decision, mode, conf, reason = "FAILCLOSED", "repair_failclosed", 0.93, "forbidden runtime/provider flag repaired to fail closed"
    elif not raw.strip():
        decision, mode, conf, reason = "BLOCKED", "fallback_classifier", 0.84, "empty or blank input cannot be admitted"
    elif ("source conflict" in low or "missing evidence" in low or "ocr" in low or "unsupported" in low):
        decision, mode, conf, reason = "BLOCKED", "fallback_classifier", 0.86, "missing evidence or source conflict blocks output"
    elif ("close out" in low or "cannot proceed" in low or "route criteria" in low or "successor route" in low):
        decision, mode, conf, reason = "CLOSEOUT", "fallback_classifier", 0.88, "successor route is not admissible"
    else:
        decision, mode, conf, reason = "READY", "fallback_classifier", 0.82, "bounded evidence appears sufficient"

    return {
        "decision": decision,
        "parse_mode": mode,
        "confidence": conf,
        "reason": reason,
        "runtime_authority_granted": False,
        "provider_dispatch_enabled": False,
        "input_preview": _preview(raw),
        "request_id": rid,
        "ts_unix": time.time()
    }

def batch_infer(rows: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    results = []
    for row in rows:
        rid = row.get("request_id") or row.get("id") or None
        result = infer(row.get("text", ""), request_id=str(rid) if rid else None)
        result["id"] = row.get("id", result["request_id"])
        results.append(result)
    return {"count": len(results), "results": results}

def append_jsonl(path: str, rows: Iterable[Dict[str, Any]]) -> None:
    import os
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
