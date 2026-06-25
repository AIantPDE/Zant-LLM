from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def test(name, condition):
    if condition:
        print(f"PASS {name}")
        return True
    print(f"FAIL {name}")
    return False

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    sys.path.insert(0, str(root / "src"))

    print("pytest dependency is optional; running stdlib fallback tests...")

    from zant_llm.governance import governance_flags, fail_closed_gate
    from zant_llm.post_release_monitoring_v1_5r import classify_hotfix_issue

    flags = governance_flags()
    audit_report = root / "reports/v1_5R/zant_llm_v1_5R_audit_report.json"
    smoke_report = root / "reports/v1_5R/zant_llm_v1_5R_post_release_audit_smoke_report.json"
    hotfix_report = root / "reports/v1_5R/zant_llm_v1_5R_hotfix_readiness_report.json"

    checks = []
    checks.append(test("flags_false", flags["runtime_authority_granted"] is False and flags["provider_dispatch_enabled"] is False))
    checks.append(test("failclosed_runtime_probe", fail_closed_gate({"requests_runtime_authority": True})["gate"] == "blocked"))
    checks.append(test("failclosed_provider_probe", fail_closed_gate({"requests_provider_dispatch": True})["gate"] == "blocked"))
    checks.append(test("forbidden_output_blocked", fail_closed_gate({"output_type": "runtime_authority_granted"})["gate"] == "blocked"))

    issue_critical = {"severity": "critical", "reproducible": True, "regression": False, "safety_related": True}
    issue_regression = {"severity": "medium", "reproducible": True, "regression": True, "safety_related": False}
    issue_backlog = {"severity": "low", "reproducible": False, "regression": False, "safety_related": False}
    checks.append(test("hotfix_candidate_triage", classify_hotfix_issue(issue_critical)["lane"] == "hotfix_candidate"))
    checks.append(test("regression_replay_triage", classify_hotfix_issue(issue_regression)["lane"] == "regression_replay_required"))
    checks.append(test("maintenance_backlog_triage", classify_hotfix_issue(issue_backlog)["lane"] == "maintenance_backlog"))

    checks.append(test("audit_report_exists", audit_report.exists()))
    checks.append(test("smoke_report_exists", smoke_report.exists()))
    checks.append(test("hotfix_report_exists", hotfix_report.exists()))

    if audit_report.exists():
        report = load_json(audit_report)
        checks.append(test("release_health_score", report.get("release_health_score") == 1.0))
        checks.append(test("blocking_zero", report.get("blocking_issues") == 0))
        checks.append(test("post_release_audit_accepted", report.get("post_release_audit_accepted") is True))
        checks.append(test("hotfix_readiness_accepted", report.get("hotfix_readiness_accepted") is True))

    if smoke_report.exists():
        smoke = load_json(smoke_report)
        checks.append(test("smoke_count", smoke.get("total") == 24))
        checks.append(test("smoke_pass_rate", smoke.get("smoke_pass_rate") == 1.0))

    passed = all(checks)
    print(f"ZANT_LLM_V1_5R_STDLIB_TESTS_PASSED={passed} total={len(checks)}")
    print("RUNTIME_AUTHORITY_GRANTED=False")
    print("PROVIDER_DISPATCH_ENABLED=False")
    return 0 if passed else 1

if __name__ == "__main__":
    raise SystemExit(main())
