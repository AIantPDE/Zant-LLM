import json, sys
from pathlib import Path
from collections import Counter
ROOT = Path(__file__).resolve().parents[1]

def main():
    log_path = ROOT/"runtime_logs/v0_10R/runtime_stress_log.jsonl"
    rows = [json.loads(x) for x in log_path.read_text(encoding="utf-8").splitlines() if x.strip()]
    ids = [r.get("request_id") for r in rows]
    unique_ids = len(ids) == len(set(ids))
    all_flags_false = all(r.get("runtime_authority_granted") is False and r.get("provider_dispatch_enabled") is False for r in rows)
    all_have_ts = all(isinstance(r.get("ts_unix"), (int,float)) for r in rows)
    all_have_decision = all(r.get("decision") in {"READY","BLOCKED","CLOSEOUT","FAILCLOSED"} for r in rows)
    counts = Counter(r.get("decision") for r in rows)
    ok = unique_ids and all_flags_false and all_have_ts and all_have_decision
    report = {
        "branch": "v0.10R-runtime-harness-stress-and-log-audit",
        "mode": "runtime-log-audit",
        "rows": len(rows),
        "request_id_unique": unique_ids,
        "all_flags_false": all_flags_false,
        "all_have_ts": all_have_ts,
        "all_have_decision": all_have_decision,
        "decision_counts": dict(counts),
        "audit_ok": ok,
        "runtime_authority_granted": False,
        "provider_dispatch_enabled": False,
    }
    out = ROOT/"reports/v0_10R/zant_llm_v0_10R_runtime_log_audit_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    if not ok:
        raise SystemExit("runtime log audit failed")
    print("ZANT_LLM_V0_10R_LOG_AUDIT_OK=True")
    print(f"LOG_ROWS={len(rows)}")
    print(f"REQUEST_ID_UNIQUE={unique_ids}")
    print(f"ALL_FLAGS_FALSE={all_flags_false}")
    print(f"REPORT={out}")
    print("RUNTIME_AUTHORITY_GRANTED=False")
    print("PROVIDER_DISPATCH_ENABLED=False")
if __name__ == "__main__":
    main()
