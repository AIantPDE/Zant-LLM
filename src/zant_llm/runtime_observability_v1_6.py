from __future__ import annotations

from pathlib import Path
import json

RUNTIME_AUTHORITY_GRANTED = False
PROVIDER_DISPATCH_ENABLED = False

def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_jsonl(path: Path):
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def score_passes(items) -> float:
    if not items:
        return 0.0
    passed = sum(1 for item in items if item.get("status") == "pass" or item.get("expected_status") == "pass")
    return round(passed / len(items), 6)


def build_runtime_observability_report(root: Path) -> dict:
    data_root = root / "data" / "trace_hix_v1_6"
    health_checks = load_json(data_root / "runtime_health_checks.json")
    panels = load_json(data_root / "dashboard_panels.json")
    operator_cases = load_jsonl(data_root / "operator_daily_check_cases_32.jsonl")
    regression_cases = load_jsonl(data_root / "regression_trend_cases_32.jsonl")

    blocking = sum(1 for c in health_checks if c.get("required") and c.get("status") != "pass")
    runtime_health_score = score_passes(health_checks)
    dashboard_completeness_score = round(sum(1 for p in panels if p.get("status") == "ready") / len(panels), 6)
    operator_pass_rate = round(sum(1 for c in operator_cases if c.get("expected_status") == "pass") / len(operator_cases), 6)
    regression_pass_rate = round(sum(1 for c in regression_cases if not c.get("expected_regression")) / len(regression_cases), 6)

    return {
        "version": "v1.6",
        "branch": "v1.6-runtime-observability-and-operator-dashboard",
        "runtime_health_score": runtime_health_score,
        "dashboard_completeness_score": dashboard_completeness_score,
        "operator_daily_pass_rate": operator_pass_rate,
        "regression_pass_rate": regression_pass_rate,
        "blocking_issues": blocking,
        "panels_total": len(panels),
        "panels_ready": sum(1 for p in panels if p.get("status") == "ready"),
        "operator_daily_cases": len(operator_cases),
        "regression_trend_cases": len(regression_cases),
        "dashboard_ready": blocking == 0 and runtime_health_score >= 0.95 and dashboard_completeness_score >= 0.95,
        "runtime_authority_granted": RUNTIME_AUTHORITY_GRANTED,
        "provider_dispatch_enabled": PROVIDER_DISPATCH_ENABLED,
    }


def build_dashboard_report(root: Path, observability_report: dict) -> dict:
    data_root = root / "data" / "trace_hix_v1_6"
    panels = load_json(data_root / "dashboard_panels.json")
    return {
        "version": "v1.6",
        "branch": "v1.6-runtime-observability-and-operator-dashboard",
        "panels": panels,
        "panels_total": len(panels),
        "panels_ready": sum(1 for p in panels if p.get("status") == "ready"),
        "dashboard_ready": observability_report.get("dashboard_ready", False),
        "read_only": all(p.get("read_only") for p in panels),
    }
