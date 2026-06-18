from __future__ import annotations
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from zant_llm.v0_8_dataset import load_heldout_eval
from zant_llm.gates.heldout_model_eval_gate_v0 import evaluate_heldout_case

def main() -> int:
    rows = load_heldout_eval()
    assert len(rows) == 180
    for r in rows:
        assert evaluate_heldout_case(r) == r['expected_decision'], r['id']
        assert r.get('runtime_authority_granted') is False
        assert r.get('provider_dispatch_enabled') is False
    print('PASS test_v0_8_dataset.py::test_heldout_count')
    print('PASS test_v0_8_gates.py::test_heldout_decision_contract')
    print('PASS test_v0_8_governance.py::test_runtime_flags_false')
    print('ZANT_LLM_V0_8_STDLIB_TESTS_PASSED=True total=3 cases=180')
    print('RUNTIME_AUTHORITY_GRANTED=False')
    print('PROVIDER_DISPATCH_ENABLED=False')
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
