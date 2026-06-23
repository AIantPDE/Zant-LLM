from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from zant_llm.rc_signoff_v1_3r import evaluate_signoff, evaluate_smoke, build_artifact_inventory

def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print('PASS ' + name)

def main():
    signoff=evaluate_signoff(ROOT)
    smoke=evaluate_smoke(ROOT)
    inv=build_artifact_inventory(ROOT)
    check('test_signoff_score', signoff['signoff_score'] == 1.0)
    check('test_smoke_pass_rate', smoke['smoke_pass_rate'] == 1.0)
    check('test_blocking_zero', signoff['blocking_issues'] == 0)
    check('test_signoff_accepted', signoff['accepted'] is True)
    check('test_smoke_accepted', smoke['accepted'] is True)
    check('test_inventory_shape', inv['artifact_count'] >= 12)
    check('test_flags_false', signoff['runtime_authority_granted'] is False and smoke['provider_dispatch_enabled'] is False)
    print('ZANT_LLM_V1_3R_STDLIB_TESTS_PASSED=True total=7')
    print('RUNTIME_AUTHORITY_GRANTED=False')
    print('PROVIDER_DISPATCH_ENABLED=False')
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
