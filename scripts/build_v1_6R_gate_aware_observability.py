import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from zant_llm.gate_aware_observability_v1_6r import build_all

def main():
    summary = build_all(ROOT)
    print("ZANT_LLM_V1_6R_GATE_AWARE_OBSERVABILITY_BUILT=True")
    print(f"GATE_READY_COUNT={summary['gate_ready_count']}")
    print(f"GATE_BLOCKED_COUNT={summary['gate_blocked_count']}")
    print(f"GATE_CLOSEOUT_COUNT={summary['gate_closeout_count']}")
    print(f"GATE_FAIL_CLOSED_COUNT={summary['gate_fail_closed_count']}")
    print(f"SUCCESSOR_HYDRATION_OK={summary['successor_hydration_ok']}")
    print(f"ACTUAL_SUCCESSOR={summary['actual_successor']}")
    print(f"RECEIPT_HASH={summary['receipt_hash']}")
    print("RUNTIME_AUTHORITY_GRANTED=False")
    print("PROVIDER_DISPATCH_ENABLED=False")
if __name__ == "__main__": main()
