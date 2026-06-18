from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from zant_llm.runtime_dashboard_v0_11 import build_dashboard, load_snapshots

def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print(f"PASS {name}")

def main():
    snapshots = load_snapshots(ROOT / "data/trace_hix_v0_11/runtime_regression_snapshot.json")
    d = build_dashboard(snapshots)
    check("test_snapshot_count", len(snapshots) == 3)
    check("test_latest_pass_rate", d["trend_summary"]["pass_rate_latest"] == 1.0)
    check("test_no_regression", d["trend_summary"]["regression_detected"] is False)
    check("test_latest_log_rows", d["trend_summary"]["latest_log_rows_match_total"] is True)
    check("test_flags_false", d["runtime_authority_granted"] is False and d["provider_dispatch_enabled"] is False)
    check("test_accepted", d["acceptance_gates"]["accepted"] is True)
    print("ZANT_LLM_V0_11_STDLIB_TESTS_PASSED=True total=6")
    print("RUNTIME_AUTHORITY_GRANTED=False")
    print("PROVIDER_DISPATCH_ENABLED=False")

if __name__ == "__main__":
    main()
