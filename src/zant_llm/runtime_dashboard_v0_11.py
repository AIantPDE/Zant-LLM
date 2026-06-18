from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

READY = "READY"
BLOCKED = "BLOCKED"
CLOSEOUT = "CLOSEOUT"
FAILCLOSED = "FAILCLOSED"

def load_snapshots(path: str | Path) -> List[Dict[str, Any]]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return data["snapshots"]

def build_dashboard(snapshots: List[Dict[str, Any]]) -> Dict[str, Any]:
    current = snapshots[-1]
    total = int(current["total"])
    distribution = {
        READY: int(current["ready"]),
        BLOCKED: int(current["blocked"]),
        CLOSEOUT: int(current["closeout"]),
        FAILCLOSED: int(current["failclosed"]),
    }
    shares = {k: round(v / total, 6) for k, v in distribution.items()}
    trend = {
        "pass_rate_min": min(float(s["pass_rate"]) for s in snapshots),
        "pass_rate_latest": float(current["pass_rate"]),
        "total_cases_latest": total,
        "regression_detected": any(float(s["pass_rate"]) < 1.0 for s in snapshots),
        "risk_level": "LOW" if all(float(s["pass_rate"]) >= 1.0 for s in snapshots) else "MEDIUM",
        "all_runtime_authority_granted_false": all(s.get("runtime_authority_granted") is False for s in snapshots),
        "all_provider_dispatch_enabled_false": all(s.get("provider_dispatch_enabled") is False for s in snapshots),
        "latest_request_id_unique": current.get("request_id_unique") is True,
        "latest_log_rows_match_total": current.get("log_rows") == current.get("total"),
    }
    accepted = (
        trend["pass_rate_latest"] >= 1.0
        and trend["all_runtime_authority_granted_false"]
        and trend["all_provider_dispatch_enabled_false"]
        and trend["latest_request_id_unique"]
        and trend["latest_log_rows_match_total"]
    )
    return {
        "branch": "v0.11-runtime-regression-dashboard",
        "source_branches": [s["branch"] for s in snapshots],
        "dashboard_version": "zant_llm_v0_11_runtime_regression_dashboard_v0",
        "snapshots": snapshots,
        "current": current,
        "trend_summary": trend,
        "decision_distribution_latest": distribution,
        "decision_share_latest": shares,
        "acceptance_gates": {
            "pass_rate_threshold": 1.0,
            "request_id_unique_required": True,
            "runtime_authority_granted_must_be_false": True,
            "provider_dispatch_enabled_must_be_false": True,
            "log_rows_must_match_total": True,
            "accepted": accepted,
        },
        "successor": "v0.12-runtime-deployment-readiness",
        "runtime_authority_granted": False,
        "provider_dispatch_enabled": False,
    }

def render_markdown(dashboard: Dict[str, Any]) -> str:
    lines = [
        "# Zant-LLM v0.11 Runtime Regression Dashboard",
        "",
        f"Branch: `{dashboard['branch']}`",
        "",
        "| Branch | Total | Pass rate | READY | BLOCKED | CLOSEOUT | FAILCLOSED |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for s in dashboard["snapshots"]:
        lines.append(
            f"| `{s['branch']}` | {s['total']} | {float(s['pass_rate']):.3f} | "
            f"{s['ready']} | {s['blocked']} | {s['closeout']} | {s['failclosed']} |"
        )
    lines += [
        "",
        f"Regression detected: **{dashboard['trend_summary']['regression_detected']}**",
        f"Risk level: **{dashboard['trend_summary']['risk_level']}**",
        f"Successor: `{dashboard['successor']}`",
        "",
    ]
    return "\n".join(lines)
