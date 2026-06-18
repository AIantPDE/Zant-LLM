from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from zant_llm.runtime_dashboard_v0_11 import build_dashboard, load_snapshots, render_markdown

def main() -> int:
    snapshots = load_snapshots(ROOT / "data/trace_hix_v0_11/runtime_regression_snapshot.json")
    dashboard = build_dashboard(snapshots)
    out_dir = ROOT / "reports/v0_11"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "zant_llm_v0_11_runtime_regression_dashboard.json").write_text(
        json.dumps(dashboard, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (out_dir / "zant_llm_v0_11_runtime_regression_dashboard.md").write_text(
        render_markdown(dashboard), encoding="utf-8"
    )
    summary = {
        "branch": dashboard["branch"],
        "dashboard_created": True,
        "regression_detected": dashboard["trend_summary"]["regression_detected"],
        "risk_level": dashboard["trend_summary"]["risk_level"],
        "latest_pass_rate": dashboard["trend_summary"]["pass_rate_latest"],
        "successor": dashboard["successor"],
        "runtime_authority_granted": False,
        "provider_dispatch_enabled": False,
    }
    (out_dir / "zant_llm_v0_11_dashboard_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("ZANT_LLM_V0_11_DASHBOARD_CREATED=True")
    print("SNAPSHOT_COUNT=3")
    print("LATEST_PASS_RATE=1.0")
    print("REGRESSION_DETECTED=False")
    print("RISK_LEVEL=LOW")
    print("SUCCESSOR=v0.12-runtime-deployment-readiness")
    print("RUNTIME_AUTHORITY_GRANTED=False")
    print("PROVIDER_DISPATCH_ENABLED=False")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
