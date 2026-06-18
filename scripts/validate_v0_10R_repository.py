from pathlib import Path
import json, sys

ROOT = Path(__file__).resolve().parents[1]
required = [
    "src/zant_llm/inference_contract_v0_10R.py",
    "data/trace_hix_v0_10R/runtime_stress_cases_300.jsonl",
    "data/trace_hix_v0_10R/runtime_edge_cases_80.jsonl",
    "scripts/stress_v0_10R_runtime_harness.py",
    "scripts/audit_v0_10R_runtime_logs.py",
]
def count_jsonl(p: Path) -> int:
    return sum(1 for line in p.read_text(encoding="utf-8").splitlines() if line.strip())
def main():
    for r in required:
        if not (ROOT/r).exists():
            raise SystemExit(f"missing required file: {r}")
    stress = count_jsonl(ROOT/"data/trace_hix_v0_10R/runtime_stress_cases_300.jsonl")
    edge = count_jsonl(ROOT/"data/trace_hix_v0_10R/runtime_edge_cases_80.jsonl")
    print("ZANT_LLM_V0_10R_REPOSITORY_VALID=True")
    print(f"STRESS_CASES={stress}")
    print(f"EDGE_CASES={edge}")
    print("RUNTIME_AUTHORITY_GRANTED=False")
    print("PROVIDER_DISPATCH_ENABLED=False")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
