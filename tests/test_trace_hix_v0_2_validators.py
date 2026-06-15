from pathlib import Path
import json

from zant_llm.validators import validate_trace_hix_case

ROOT = Path(__file__).resolve().parents[1]


def _read_first(path: str):
    with (ROOT / path).open("r", encoding="utf-8") as f:
        return json.loads(next(line for line in f if line.strip()))


def test_gold_case_passes():
    case = _read_first("data/trace_hix_v0_2/gold_seed_30.jsonl")
    result = validate_trace_hix_case(case)
    assert result["all_hard_gates_pass"] is True


def test_negative_case_fails():
    case = _read_first("data/trace_hix_v0_2/negative_seed_30.jsonl")
    result = validate_trace_hix_case(case)
    assert result["all_hard_gates_pass"] is False
    assert result["rejection_reasons"]
