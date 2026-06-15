from __future__ import annotations
import argparse, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"src"))
from zant_llm.validators.reference_closure_validator_v0 import validate_reference_closure
from zant_llm.validators.claim_support_validator_v0 import validate_claim_support
from zant_llm.validators.forbidden_output_scanner_v0 import validate_forbidden_output
from zant_llm.validators.authority_leakage_scanner_v0 import validate_authority_leakage

def load_jsonl(path: Path) -> list[dict]: return [json.loads(line) for line in path.open("r", encoding="utf-8") if line.strip()]
def validate(case, exp):
    reports=[validate_reference_closure(case["bundle"], exp), validate_claim_support(case["bundle"], exp), validate_forbidden_output(exp), validate_authority_leakage(exp)]
    return {"case_id":case["case_id"],"all_hard_gates_pass":all(r["passed"] for r in reports),"reports":reports}
def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("--mode", choices=["contract","model"], default="contract"); ap.add_argument("--eval-cases", default=str(ROOT/"data/trace_hix_v0_3/trace_hix_v0_3_eval_cases_12.jsonl")); ap.add_argument("--base-model", default=r"D:\gemma-4-E2B-it"); ap.add_argument("--adapter-path", default=str(ROOT/"outputs/v0_3/gemma4_qlora_adapter")); ap.add_argument("--output-report", default=str(ROOT/"reports/v0_3/zant_llm_v0_3_eval_report.json")); args=ap.parse_args()
    cases=load_jsonl(Path(args.eval_cases))
    if args.mode == "model":
        raise SystemExit("Model eval scaffold is present, but v0.3 package defaults to contract eval. Use generated adapter and extend this runner after local training.")
    results=[validate(c, c["target_explanation"]) for c in cases]
    passed=sum(1 for r in results if r["all_hard_gates_pass"])
    report={"report_version":"zant_llm_v0_3_eval_report_v0","mode":args.mode,"eval_cases":len(cases),"passed_cases":passed,"failed_cases":len(cases)-passed,"hard_gate_pass_rate":passed/len(cases) if cases else 0.0,"runtime_authority_granted":False,"provider_dispatch_enabled":False,"results":results}
    out=Path(args.output_report); out.parent.mkdir(parents=True, exist_ok=True); out.write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print("ZANT_LLM_V0_3_EVALUATED=True"); print(f"MODE={args.mode}"); print(f"HARD_GATE_PASS_RATE={report['hard_gate_pass_rate']}"); print(f"REPORT={out}"); print("RUNTIME_AUTHORITY_GRANTED=False"); print("PROVIDER_DISPATCH_ENABLED=False")
    return 0
if __name__ == "__main__": raise SystemExit(main())
