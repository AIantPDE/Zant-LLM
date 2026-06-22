from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from zant_llm.release_candidate_v1_3 import evaluate_release_candidate, build_artifact_inventory

def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print('PASS ' + name)

def main():
    report = evaluate_release_candidate(ROOT)
    inv = build_artifact_inventory(ROOT)
    check('test_rc_score', report['rc_score'] == 1.0)
    check('test_blocking_zero', report['blocking_issues'] == 0)
    check('test_accepted', report['accepted'] is True)
    check('test_inventory_shape', inv['artifact_count'] >= 10)
    check('test_flags_false', report['runtime_authority_granted'] is False and report['provider_dispatch_enabled'] is False)
    print('ZANT_LLM_V1_3_STDLIB_TESTS_PASSED=True total=5')
    print('RUNTIME_AUTHORITY_GRANTED=False')
    print('PROVIDER_DISPATCH_ENABLED=False')
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
