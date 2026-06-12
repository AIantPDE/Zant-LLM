import json
from pathlib import Path

from zant_llm.schema import validate_record


def test_seed_records_are_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    path = root / "data/seed/zant_llm_v0_1_seed_30.jsonl"
    records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]
    assert len(records) == 30
    for record in records:
        validate_record(record)
