from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ["VERSION","README.md","src/zant_llm/governance.py","src/zant_llm/orsc_v6_gate.py","src/zant_llm/gate_aware_observability_v1_6r.py","src/zant_llm/successor_resolution_v1_6r.py","data/trace_hix_v1_6R/gate_cases_ready_blocked_closeout.jsonl","data/trace_hix_v1_6R/successor_hydration_cases.jsonl","data/trace_hix_v1_6R/receipt_cases.jsonl","data/trace_hix_v1_6R/negative_authority_cases.jsonl","data/trace_hix_v1_6R/dashboard_gate_panels.json","registries/gate_result_taxonomy_v0.json","registries/forbidden_output_registry_v0.json","registries/orsc_v6_gate_registry_v0.json","registries/successor_resolution_registry_v0.json"]
def count_jsonl(path: Path) -> int:
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
def main() -> None:
    missing = [p for p in REQUIRED if not (ROOT / p).exists()]
    if missing: raise SystemExit("Missing required files: " + ", ".join(missing))
    gate_cases = count_jsonl(ROOT / "data/trace_hix_v1_6R/gate_cases_ready_blocked_closeout.jsonl")
    hydration_cases = count_jsonl(ROOT / "data/trace_hix_v1_6R/successor_hydration_cases.jsonl")
    receipt_cases = count_jsonl(ROOT / "data/trace_hix_v1_6R/receipt_cases.jsonl")
    negative_cases = count_jsonl(ROOT / "data/trace_hix_v1_6R/negative_authority_cases.jsonl")
    panel_count = len(json.loads((ROOT / "data/trace_hix_v1_6R/dashboard_gate_panels.json").read_text(encoding="utf-8")))
    assert gate_cases == 36; assert hydration_cases == 24; assert receipt_cases == 18; assert negative_cases == 24; assert panel_count == 10
    print(f"[Zant-LLM v1.6R] repository root: {ROOT}")
    print("ZANT_LLM_V1_6R_REPOSITORY_VALID=True")
    print(f"GATE_CASES={gate_cases}")
    print(f"SUCCESSOR_HYDRATION_CASES={hydration_cases}")
    print(f"RECEIPT_CASES={receipt_cases}")
    print(f"NEGATIVE_AUTHORITY_CASES={negative_cases}")
    print(f"DASHBOARD_GATE_PANELS={panel_count}")
    print("RUNTIME_AUTHORITY_GRANTED=False")
    print("PROVIDER_DISPATCH_ENABLED=False")
if __name__ == "__main__": main()
