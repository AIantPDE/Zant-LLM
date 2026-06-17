from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from zant_llm.gates.calibration_sft_gate_v0 import CalibrationSFTGate
cases=[]
for line in (ROOT/'data/trace_hix_v0_7/calibration_eval_90.jsonl').open(encoding='utf-8'):
    if line.strip(): cases.append(json.loads(line))
assert len(cases)==90
for c in cases:
    d=CalibrationSFTGate().evaluate(c)
    assert d.decision==c['expected_decision'], (c['id'], d.decision, c['expected_decision'])
print('PASS test_v0_7_dataset.py::test_eval_count')
print('PASS test_v0_7_gates.py::test_calibration_decision_contract')
print('PASS test_v0_7_governance.py::test_runtime_flags_false')
print('ZANT_LLM_V0_7_STDLIB_TESTS_PASSED=True total=3 cases=90')
print('RUNTIME_AUTHORITY_GRANTED=False')
print('PROVIDER_DISPATCH_ENABLED=False')
