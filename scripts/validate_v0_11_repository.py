from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def count_snapshots() -> int:
    p = ROOT / "data/trace_hix_v0_11/runtime_regression_snapshot.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    return len(data["snapshots"])

def main() -> int:
    required = [
        "README.md",
        "src/zant_llm/runtime_dashboard_v0_11.py",
        "data/trace_hix_v0_11/runtime_regression_snapshot.json",
        "scripts/build_v0_11_runtime_regression_dashboard.py",
        "reports/v0_11/zant_llm_v0_11_runtime_regression_dashboard.json",
    ]
    missing = [p for p in required if not (ROOT / p).exists()]
    if missing:
        raise AssertionError("missing required files: " + ", ".join(missing))
    snapshots = count_snapshots()
    if snapshots < 3:
        raise AssertionError("expected at least 3 runtime snapshots")
    print("ZANT_LLM_V0_11_REPOSITORY_VALID=True")
    print(f"SNAPSHOT_COUNT={snapshots}")
    print("LATEST_BRANCH=v0.10R-runtime-harness-stress-and-log-audit")
    print("RUNTIME_AUTHORITY_GRANTED=False")
    print("PROVIDER_DISPATCH_ENABLED=False")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
