from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from zant_llm.validators import validate_trace_hix_case

DATA_PATHS = [
    ROOT / "data/trace_hix_v0_2/gold_seed_30.jsonl",
    ROOT / "data/trace_hix_v0_2/negative_seed_30.jsonl",
]
REPORT_DIR = ROOT / "reports/v0_2"


def read_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def main() -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    report_family = defaultdict(list)
    mismatches = []
    for path in DATA_PATHS:
        for case in read_jsonl(path):
            result = validate_trace_hix_case(case)
            expected_valid = case.get("expected", {}).get("valid")
            if result["all_hard_gates_pass"] != expected_valid:
                mismatches.append({"case_id": case.get("case_id"), "expected_valid": expected_valid, "actual": result["all_hard_gates_pass"], "reasons": result["rejection_reasons"]})
            results.append(result)
            for report in result["reports"]:
                report_family[report["name"]].append({"case_id": result["case_id"], **report})
    for name, rows in report_family.items():
        out = {"report_name": name, "report_version": name, "case_count": len(rows), "rows": rows}
        (REPORT_DIR / f"{name}.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    reason_counts = Counter(reason for r in results for reason in r["rejection_reasons"])
    summary = {
        "summary_version":"trace_hix_v0_2_validation_summary",
        "total_cases":len(results),
        "passed_cases":sum(1 for r in results if r["all_hard_gates_pass"]),
        "failed_cases":sum(1 for r in results if not r["all_hard_gates_pass"]),
        "reason_counts":dict(reason_counts),
        "mismatches":mismatches,
        "all_expectations_met":not mismatches,
        "runtime_authority_granted":False,
        "provider_dispatch_enabled":False,
    }
    (REPORT_DIR / "trace_hix_v0_2_validation_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print("TRACE_HIX_V0_2_VALIDATORS_RAN=True")
    print(f"TOTAL_CASES={summary['total_cases']}")
    print(f"PASSED_CASES={summary['passed_cases']}")
    print(f"FAILED_CASES={summary['failed_cases']}")
    print(f"ALL_EXPECTATIONS_MET={summary['all_expectations_met']}")
    print("RUNTIME_AUTHORITY_GRANTED=False")
    print("PROVIDER_DISPATCH_ENABLED=False")
    if mismatches:
        print(json.dumps(mismatches, ensure_ascii=False, indent=2))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
