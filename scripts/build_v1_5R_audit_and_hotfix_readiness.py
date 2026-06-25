from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT_IMPORT_HINT = "src"

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows

def write_json(path: Path, data: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def build_sha256_summary(root: Path) -> list[str]:
    lines = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if rel == "SHA256SUMS.txt" or rel.startswith(".git/") or "__pycache__" in rel:
            continue
        lines.append(f"{sha256_file(path)}  {rel}")
    (root / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return lines

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    sys.path.insert(0, str(root / ROOT_IMPORT_HINT))

    from zant_llm.governance import fail_closed_gate
    from zant_llm.post_release_monitoring_v1_5r import compute_audit_result, classify_hotfix_issue

    audit_checks = load_json(root / "data/trace_hix_v1_5R/audit_checks.json")
    hotfix_checks = load_json(root / "data/trace_hix_v1_5R/hotfix_readiness_checks.json")
    smoke_cases = load_jsonl(root / "data/trace_hix_v1_5R/post_release_audit_smoke_cases_24.jsonl")
    regression_cases = load_jsonl(root / "data/trace_hix_v1_5R/regression_replay_cases_24.jsonl")

    result = compute_audit_result(audit_checks, smoke_cases, hotfix_checks, regression_cases).to_dict()
    report = {
        "version": "v1.5R",
        "branch": "v1.5R-post-release-monitoring-audit-and-hotfix-readiness",
        "baseline": "v1.5-post-release-monitoring-and-maintenance",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        **result,
        "counts": {
            "audit_checks": len(audit_checks),
            "hotfix_readiness_checks": len(hotfix_checks),
            "smoke_cases": len(smoke_cases),
            "regression_replay_cases": len(regression_cases),
        },
    }

    smoke_passed = 0
    blocked_probes = 0
    smoke_details = []
    for row in smoke_cases:
        gate = fail_closed_gate(row)
        expected_gate = row.get("expected_gate", "pass")
        ok = gate["gate"] == expected_gate or (expected_gate == "blocked" and gate["gate"] == "blocked")
        smoke_passed += int(ok)
        blocked_probes += int(gate["gate"] == "blocked")
        smoke_details.append({
            "id": row["id"],
            "expected_gate": expected_gate,
            "actual_gate": gate["gate"],
            "passed": ok,
            "reasons": gate["reasons"],
        })

    smoke_report = {
        "version": "v1.5R",
        "total": len(smoke_cases),
        "passed": smoke_passed,
        "blocked_probes": blocked_probes,
        "smoke_pass_rate": round(smoke_passed / len(smoke_cases), 6) if smoke_cases else 0.0,
        "details": smoke_details,
        "runtime_authority_granted": False,
        "provider_dispatch_enabled": False,
    }

    sample_triage = [
        {"severity": "critical", "reproducible": True, "regression": False, "safety_related": True},
        {"severity": "medium", "reproducible": True, "regression": True, "safety_related": False},
        {"severity": "low", "reproducible": False, "regression": False, "safety_related": False},
    ]
    triage = [classify_hotfix_issue(issue) for issue in sample_triage]
    hotfix_report = {
        "version": "v1.5R",
        "hotfix_readiness_score": report["hotfix_readiness_score"],
        "hotfix_readiness_accepted": report["hotfix_readiness_accepted"],
        "triage_lanes": sorted({row["lane"] for row in triage}),
        "triage_examples": triage,
        "runtime_authority_granted": False,
        "provider_dispatch_enabled": False,
    }

    report_dir = root / "reports/v1_5R"
    write_json(report_dir / "zant_llm_v1_5R_audit_report.json", report)
    write_json(report_dir / "zant_llm_v1_5R_post_release_audit_smoke_report.json", smoke_report)
    write_json(report_dir / "zant_llm_v1_5R_hotfix_readiness_report.json", hotfix_report)

    inventory = {
        "version": "v1.5R",
        "artifacts": sorted(
            str(p.relative_to(root)).replace("\\", "/")
            for p in root.rglob("*")
            if p.is_file() and ".git" not in p.parts and "__pycache__" not in p.parts
        ),
    }
    write_json(report_dir / "zant_llm_v1_5R_artifact_inventory.json", inventory)

    summary = f"""# Zant-LLM v1.5R Audit Summary

- RELEASE_HEALTH_SCORE={report['release_health_score']}
- SMOKE_PASS_RATE={report['smoke_pass_rate']}
- AUDIT_PASS_RATE={report['audit_pass_rate']}
- HOTFIX_READINESS_SCORE={report['hotfix_readiness_score']}
- REGRESSION_REPLAY_PASS_RATE={report['regression_replay_pass_rate']}
- BLOCKING_ISSUES={report['blocking_issues']}
- POST_RELEASE_AUDIT_ACCEPTED={report['post_release_audit_accepted']}
- HOTFIX_READINESS_ACCEPTED={report['hotfix_readiness_accepted']}
- RUNTIME_AUTHORITY_GRANTED=False
- PROVIDER_DISPATCH_ENABLED=False
"""
    write_text(report_dir / "zant_llm_v1_5R_audit_summary.md", summary)

    build_sha256_summary(root)

    print("ZANT_LLM_V1_5R_AUDIT_AND_HOTFIX_BUILT=True")
    print(f"RELEASE_HEALTH_SCORE={report['release_health_score']}")
    print(f"SMOKE_PASS_RATE={smoke_report['smoke_pass_rate']}")
    print(f"AUDIT_PASS_RATE={report['audit_pass_rate']}")
    print(f"HOTFIX_READINESS_SCORE={report['hotfix_readiness_score']}")
    print(f"REGRESSION_REPLAY_PASS_RATE={report['regression_replay_pass_rate']}")
    print(f"BLOCKING_ISSUES={report['blocking_issues']}")
    print(f"POST_RELEASE_AUDIT_ACCEPTED={report['post_release_audit_accepted']}")
    print(f"HOTFIX_READINESS_ACCEPTED={report['hotfix_readiness_accepted']}")
    print(f"REPORT={report_dir / 'zant_llm_v1_5R_audit_report.json'}")
    print("RUNTIME_AUTHORITY_GRANTED=False")
    print("PROVIDER_DISPATCH_ENABLED=False")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
