from pathlib import Path
import json, sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from zant_llm.v0_6R_calibration import summarize, recommend_successor
def load_jsonl(path): return [json.loads(x) for x in path.read_text(encoding='utf-8').splitlines() if x.strip()]
def main():
    rows = load_jsonl(ROOT/'data/trace_hix_v0_6R/v0_6_realworld_eval_snapshot_300.jsonl')
    s=summarize(rows)
    assert len(rows)==300
    assert s['decision_counts']['READY']==45
    assert s['decision_counts']['BLOCKED']==138
    assert s['decision_counts']['CLOSEOUT']==9
    assert s['decision_counts']['FAILCLOSED']==108
    assert s['pass_rate']==1.0
    assert recommend_successor(s)['successor']=='READY_TO_V0_7_CALIBRATION_SFT'
    print('PASS test_v0_6R_calibration.py::test_distribution')
    print('PASS test_v0_6R_calibration.py::test_successor_recommendation')
    print('ZANT_LLM_V0_6R_STDLIB_TESTS_PASSED=True total=2 cases=300')
    print('RUNTIME_AUTHORITY_GRANTED=False')
    print('PROVIDER_DISPATCH_ENABLED=False')
    return 0
if __name__ == '__main__': raise SystemExit(main())
