import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from zant_llm.gate_aware_observability_v1_6r import PROPOSED_SUCCESSOR, FALLBACK_SUCCESSOR

def main():
    report_path = ROOT / "reports/v1_6R/zant_llm_v1_6R_gate_aware_observability_report.json"
    summary = json.loads(report_path.read_text(encoding="utf-8")) if report_path.exists() else {"ok": False}
    adopted = bool(summary.get("ok")) and summary.get("actual_successor") == PROPOSED_SUCCESSOR
    out = {"schema":"ZANT_LLM_V1_6R_SUCCESSOR_RECOMMENDATION_V0", "ok": True, "proposed_successor": PROPOSED_SUCCESSOR, "actual_successor": PROPOSED_SUCCESSOR if adopted else FALLBACK_SUCCESSOR, "adopted": adopted, "reason":"gate-aware observability and receipt hardening complete" if adopted else "v1.6R gate-aware closure incomplete"}
    p = ROOT / "reports/v1_6R/zant_llm_v1_6R_successor_recommendation.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(out, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print("ZANT_LLM_V1_6R_SUCCESSOR_RECOMMENDATION_CREATED=True")
    print(f"ACTUAL_SUCCESSOR={out['actual_successor']}")
    print(f"REPORT={p}")
if __name__ == "__main__": main()
