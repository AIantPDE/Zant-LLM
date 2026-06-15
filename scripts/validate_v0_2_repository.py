from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "GOVERNANCE.md",
    "schemas/trace_hix_drl_decision_explanation_bundle_v0.schema.json",
    "schemas/trace_hix_human_explanation_preview_v0.schema.json",
    "schemas/trace_hix_claim_atom_v0.schema.json",
    "registries/forbidden_output_registry_v0.json",
    "registries/allowed_predicate_registry_v0.json",
    "registries/rejection_reason_taxonomy_v0.json",
    "data/trace_hix_v0_2/gold_seed_30.jsonl",
    "data/trace_hix_v0_2/negative_seed_30.jsonl",
]


def read_jsonl(path: Path):
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise AssertionError(f"invalid jsonl {path}:{line_no}: {exc}") from exc
    return rows


def main() -> int:
    missing = [p for p in REQUIRED_FILES if not (ROOT / p).exists()]
    if missing:
        raise AssertionError(f"missing required files: {missing}")
    gold = read_jsonl(ROOT / "data/trace_hix_v0_2/gold_seed_30.jsonl")
    negative = read_jsonl(ROOT / "data/trace_hix_v0_2/negative_seed_30.jsonl")
    assert len(gold) == 30, f"gold count expected 30 got {len(gold)}"
    assert len(negative) == 30, f"negative count expected 30 got {len(negative)}"
    for row in gold:
        assert row.get("expected", {}).get("valid") is True, f"gold expected invalid: {row.get('case_id')}"
    for row in negative:
        assert row.get("expected", {}).get("valid") is False, f"negative expected valid: {row.get('case_id')}"
    print("TRACE_HIX_V0_2_REPOSITORY_VALID=True")
    print(f"GOLD_SEED_COUNT={len(gold)}")
    print(f"NEGATIVE_SEED_COUNT={len(negative)}")
    print("RUNTIME_AUTHORITY_GRANTED=False")
    print("PROVIDER_DISPATCH_ENABLED=False")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
