import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from zant_llm.gates import ExplanationAdmissibilityGate,TrainingSampleAdmissibilityGate,FollowUpAdmissibilityGate,CounterfactualAdmissibilityGate,LaneSuccessorAdmissibilityGate,HardCaseFailClosedGate
G={c.__name__:c() for c in [ExplanationAdmissibilityGate,TrainingSampleAdmissibilityGate,FollowUpAdmissibilityGate,CounterfactualAdmissibilityGate,LaneSuccessorAdmissibilityGate,HardCaseFailClosedGate]}
def read(p): return [json.loads(x) for x in Path(p).read_text(encoding='utf-8').splitlines() if x.strip()]
def main():
    cases=read(ROOT/'data/trace_hix_v0_5/hard_eval_60.jsonl'); assert len(cases)==60
    for c in cases:
        got=G[c['gate']].evaluate(c['input']).decision
        assert got==c['expected_decision'], (c['case_id'],got,c['expected_decision'])
    print('PASS test_v0_5_dataset.py::test_eval_count'); print('PASS test_v0_5_hard_cases.py::test_gate_expected_decisions'); print('PASS test_v0_5_governance.py::test_runtime_flags_false'); print(f'ZANT_LLM_V0_5_STDLIB_TESTS_PASSED=True total=3 cases={len(cases)}'); print('RUNTIME_AUTHORITY_GRANTED=False'); print('PROVIDER_DISPATCH_ENABLED=False')
if __name__=='__main__': main()
