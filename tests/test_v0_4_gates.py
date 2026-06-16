from pathlib import Path
from zant_llm.v0_4_dataset import load_jsonl
from zant_llm.gates import ExplanationAdmissibilityGate
ROOT=Path(__file__).resolve().parents[1]
def test_first_gate_matches():
    row=load_jsonl(ROOT/'data/trace_hix_v0_4/train_cases_180.jsonl')[0]
    assert ExplanationAdmissibilityGate().evaluate(row).decision == row['gate_result']
