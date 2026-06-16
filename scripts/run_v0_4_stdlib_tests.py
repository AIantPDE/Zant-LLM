import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from zant_llm.v0_4_dataset import load_jsonl, to_sft
from zant_llm.governance import assert_boundaries
from zant_llm.gates import ExplanationAdmissibilityGate
def main():
    train=load_jsonl(ROOT/'data/trace_hix_v0_4/train_cases_180.jsonl'); ev=load_jsonl(ROOT/'data/trace_hix_v0_4/eval_cases_45.jsonl')
    assert len(train)==180; print('PASS test_v0_4_dataset.py::test_train_count')
    assert len(ev)==45; print('PASS test_v0_4_dataset.py::test_eval_count')
    assert 'OUTPUT_JSON' in to_sft(train[0])['text']; print('PASS test_v0_4_dataset.py::test_sft_format')
    assert_boundaries(); print('PASS test_v0_4_governance.py::test_runtime_flags_false')
    assert ExplanationAdmissibilityGate().evaluate(train[0]).decision==train[0]['gate_result']; print('PASS test_v0_4_gates.py::test_gate_decision_matches')
    print('ZANT_LLM_V0_4_STDLIB_TESTS_PASSED=True total=5'); return 0
if __name__=='__main__': raise SystemExit(main())

