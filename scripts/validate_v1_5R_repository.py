from __future__ import annotations

import argparse
import compileall
import json
import sys
from pathlib import Path

REQUIRED_FILES = [
    "README.md",
    "VERSION",
    "GOVERNANCE.md",
    "SECURITY.md",
    "RELEASE_POLICY.md",
    "requirements-v1.5R.txt",
    "src/zant_llm/__init__.py",
    "src/zant_llm/governance.py",
    "src/zant_llm/post_release_monitoring_v1_5r.py",
    "data/trace_hix_v1_5R/audit_checks.json",
    "data/trace_hix_v1_5R/hotfix_readiness_checks.json",
    "data/trace_hix_v1_5R/post_release_audit_smoke_cases_24.jsonl",
    "data/trace_hix_v1_5R/regression_replay_cases_24.jsonl",
    "data/trace_hix_v1_5R/issue_audit_template.json",
    "data/trace_hix_v1_5R/hotfix_intake_template.json",
    "data_manifests/zant_llm_v1_5R_data_manifest.json",
    "docs/V1_5R_POST_RELEASE_MONITORING_AUDIT_AND_HOTFIX_READINESS.md",
    "docs/POST_RELEASE_AUDIT_CHECKLIST.md",
    "docs/HOTFIX_READINESS_CHECKLIST.md",
    "docs/REGRESSION_REPLAY_POLICY.md",
    "docs/ISSUE_INTAKE_AUDIT_GUIDE.md",
    "docs/HOTFIX_BRANCH_POLICY.md",
    "registries/forbidden_output_registry_v0.json",
    "registries/gate_result_taxonomy_v0.json",
    "registries/post_release_audit_registry_v0.json",
    "registries/hotfix_readiness_registry_v0.json",
    "schemas/zant_llm_v1_5R_audit_report_v0.schema.json",
    "schemas/zant_llm_v1_5R_smoke_report_v0.schema.json",
    "schemas/zant_llm_v1_5R_hotfix_readiness_report_v0.schema.json",
    "schemas/zant_llm_v1_5R_successor_recommendation_v0.schema.json",
    "scripts/build_v1_5R_audit_and_hotfix_readiness.py",
    "scripts/make_v1_5R_release_manifest.py",
    "scripts/make_v1_5R_successor_recommendation.py",
    "scripts/run_v1_5R_stdlib_tests.py",
]

def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def count_jsonl(path: Path) -> int:
    with path.open("r", encoding="utf-8") as f:
        return sum(1 for line in f if line.strip())

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()

    print(f"[Zant-LLM v1.5R] repository root: {root}")

    missing = [p for p in REQUIRED_FILES if not (root / p).exists()]
    if missing:
        print("ZANT_LLM_V1_5R_REPOSITORY_VALID=False")
        print("MISSING_FILES=" + json.dumps(missing, ensure_ascii=False))
        return 1

    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    audit_checks = read_json(root / "data/trace_hix_v1_5R/audit_checks.json")
    hotfix_checks = read_json(root / "data/trace_hix_v1_5R/hotfix_readiness_checks.json")
    smoke_cases = count_jsonl(root / "data/trace_hix_v1_5R/post_release_audit_smoke_cases_24.jsonl")
    regression_cases = count_jsonl(root / "data/trace_hix_v1_5R/regression_replay_cases_24.jsonl")

    flags_text = (root / "src/zant_llm/governance.py").read_text(encoding="utf-8")
    runtime_false = "RUNTIME_AUTHORITY_GRANTED = False" in flags_text
    provider_false = "PROVIDER_DISPATCH_ENABLED = False" in flags_text

    compile_ok = compileall.compile_dir(str(root / "src"), quiet=1)
    compile_ok = compileall.compile_dir(str(root / "scripts"), quiet=1) and compile_ok

    valid = (
        version == "v1.5R"
        and len(audit_checks) == 24
        and len(hotfix_checks) == 24
        and smoke_cases == 24
        and regression_cases == 24
        and runtime_false
        and provider_false
        and compile_ok
    )

    print(f"ZANT_LLM_V1_5R_REPOSITORY_VALID={valid}")
    print(f"AUDIT_CHECKS={len(audit_checks)}")
    print(f"HOTFIX_READINESS_CHECKS={len(hotfix_checks)}")
    print(f"SMOKE_CASES={smoke_cases}")
    print(f"REGRESSION_REPLAY_CASES={regression_cases}")
    print("RUNTIME_AUTHORITY_GRANTED=False")
    print("PROVIDER_DISPATCH_ENABLED=False")

    return 0 if valid else 1

if __name__ == "__main__":
    raise SystemExit(main())
