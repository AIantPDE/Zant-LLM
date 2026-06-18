import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def main():
    stress = json.loads((ROOT/"reports/v0_10R/zant_llm_v0_10R_runtime_stress_report.json").read_text(encoding="utf-8"))
    audit = json.loads((ROOT/"reports/v0_10R/zant_llm_v0_10R_runtime_log_audit_report.json").read_text(encoding="utf-8"))
    successor = "v0.11-runtime-regression-dashboard" if stress["stress_pass_rate"] == 1.0 and audit["audit_ok"] else "v0.10R2-runtime-harness-fix"
    report = {
        "branch": "v0.10R-runtime-harness-stress-and-log-audit",
        "successor": successor,
        "reason": "stress and runtime log audit passed" if successor.startswith("v0.11") else "stress or log audit needs repair",
        "runtime_authority_granted": False,
        "provider_dispatch_enabled": False,
    }
    out = ROOT/"reports/v0_10R/zant_llm_v0_10R_successor_recommendation.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("ZANT_LLM_V0_10R_SUCCESSOR_RECOMMENDATION_CREATED=True")
    print(f"SUCCESSOR={successor}")
    print(f"REPORT={out}")
if __name__ == "__main__":
    main()
