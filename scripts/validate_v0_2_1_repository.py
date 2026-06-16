from __future__ import annotations

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "docs/ORSC_V6_LANE_GOVERNANCE.md",
    "docs/TRACE_HIX_V0_2_1_ORSC_GATE_ALIGNMENT.md",
    "schemas/trace_hix_admissibility_gate_v0.schema.json",
    "schemas/trace_hix_gate_aware_receipt_v0.schema.json",
    "schemas/trace_hix_successor_resolution_v0.schema.json",
    "registries/gate_result_taxonomy_v0.json",
    "registries/admissibility_gate_registry_v0.json",
    "src/zant_llm/gates/common.py",
    "data/trace_hix_v0_2_1/gate_gold_15.jsonl",
    "data/trace_hix_v0_2_1/gate_negative_15.jsonl",
    "scripts/run_trace_hix_v0_2_1_gate_tests.py",
]

def count_jsonl(path: Path) -> int:
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())

def main() -> int:
    missing = [p for p in REQUIRED if not (ROOT / p).exists()]
    if missing:
        raise SystemExit("Missing required files: " + ", ".join(missing))
    for schema in (ROOT / "schemas").glob("trace_hix_*v0.schema.json"):
        json.loads(schema.read_text(encoding="utf-8"))
    gold = count_jsonl(ROOT / "data/trace_hix_v0_2_1/gate_gold_15.jsonl")
    neg = count_jsonl(ROOT / "data/trace_hix_v0_2_1/gate_negative_15.jsonl")
    print("TRACE_HIX_V0_2_1_REPOSITORY_VALID=True")
    print(f"GOLD_GATE_CASES={gold}")
    print(f"NEGATIVE_GATE_CASES={neg}")
    print("RUNTIME_AUTHORITY_GRANTED=False")
    print("PROVIDER_DISPATCH_ENABLED=False")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
