import json, sys, time
from pathlib import Path
from collections import Counter
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"src"))
from zant_llm.inference_contract_v0_10R import infer, append_jsonl

def load_jsonl(path):
    return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]

def main():
    stress = load_jsonl(ROOT/"data/trace_hix_v0_10R/runtime_stress_cases_300.jsonl")
    edge = load_jsonl(ROOT/"data/trace_hix_v0_10R/runtime_edge_cases_80.jsonl")
    rows = stress + edge
    results = []
    counts = Counter()
    ok = 0
    log_path = ROOT/"runtime_logs/v0_10R/runtime_stress_log.jsonl"
    if log_path.exists():
        log_path.unlink()
    for row in rows:
        res = infer(row.get("text",""))
        res["id"] = row["id"]
        res["expected"] = row["expected"]
        res["family"] = row.get("family")
        res["ok"] = res["decision"] == row["expected"] and res["runtime_authority_granted"] is False and res["provider_dispatch_enabled"] is False
        ok += 1 if res["ok"] else 0
        counts[res["decision"]] += 1
        results.append(res)
    append_jsonl(str(log_path), results)
    report = {
        "branch": "v0.10R-runtime-harness-stress-and-log-audit",
        "mode": "runtime-harness-stress",
        "total": len(rows),
        "correct": ok,
        "stress_pass_rate": ok / len(rows),
        "decision_counts": dict(counts),
        "runtime_log": str(log_path),
        "runtime_authority_granted": False,
        "provider_dispatch_enabled": False,
    }
    out = ROOT/"reports/v0_10R/zant_llm_v0_10R_runtime_stress_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("ZANT_LLM_V0_10R_STRESS_OK=True")
    print(f"STRESS_TOTAL={len(rows)}")
    print(f"STRESS_PASS_RATE={report['stress_pass_rate']}")
    for k in ["READY","BLOCKED","CLOSEOUT","FAILCLOSED"]:
        print(f"{k}_COUNT={counts.get(k,0)}")
    print(f"REPORT={out}")
    print("RUNTIME_AUTHORITY_GRANTED=False")
    print("PROVIDER_DISPATCH_ENABLED=False")
if __name__ == "__main__":
    main()
