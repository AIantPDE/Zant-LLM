from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from zant_llm.gates import (  # noqa: E402
    CounterfactualAdmissibilityGate,
    ExplanationAdmissibilityGate,
    FollowUpAdmissibilityGate,
    LaneSuccessorAdmissibilityGate,
    TrainingSampleAdmissibilityGate,
)

GATES = {
    "ExplanationAdmissibilityGate": ExplanationAdmissibilityGate(),
    "TrainingSampleAdmissibilityGate": TrainingSampleAdmissibilityGate(),
    "FollowUpAdmissibilityGate": FollowUpAdmissibilityGate(),
    "CounterfactualAdmissibilityGate": CounterfactualAdmissibilityGate(),
    "LaneSuccessorAdmissibilityGate": LaneSuccessorAdmissibilityGate(),
}


def read_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def main() -> int:
    rows = list(read_jsonl(ROOT / "data/trace_hix_v0_2_1/gate_gold_15.jsonl"))
    rows += list(read_jsonl(ROOT / "data/trace_hix_v0_2_1/gate_negative_15.jsonl"))
    passed = 0
    failed = 0
    results = []
    for row in rows:
        gate = GATES[row["gate"]]
        decision = gate.evaluate(row["payload"]).to_dict()
        ok = decision["decision"] == row["expected"]
        passed += int(ok)
        failed += int(not ok)
        results.append({"case_id": row["id"], "gate": row["gate"], "expected": row["expected"], "actual": decision["decision"], "ok": ok, "decision": decision})
        print(("PASS" if ok else "FAIL") + f" {row['id']} {row['gate']} expected={row['expected']} actual={decision['decision']}")
    report_dir = ROOT / "reports/v0_2_1"
    report_dir.mkdir(parents=True, exist_ok=True)
    report = {
        "report_version": "trace_hix_v0_2_1_gate_test_report_v0",
        "total": len(rows),
        "passed": passed,
        "failed": failed,
        "runtime_authority_granted": False,
        "provider_dispatch_enabled": False,
        "results": results,
    }
    (report_dir / "trace_hix_v0_2_1_gate_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(f"TRACE_HIX_V0_2_1_GATE_TESTS_PASSED={failed == 0} total={len(rows)}")
    print("RUNTIME_AUTHORITY_GRANTED=False")
    print("PROVIDER_DISPATCH_ENABLED=False")
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    raise SystemExit(main())
