from pathlib import Path
import sys, json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from zant_llm.deployment_readiness_v1_2 import evaluate_readiness, build_artifact_inventory
from zant_llm.governance import governance_flags
def run(name, fn): fn(); print('PASS', name)
def test_readiness_score():
    r=evaluate_readiness(ROOT); assert r['readiness_score']==1.0 and r['blocking_issues']==0 and r['accepted'] is True, r
def test_inventory_shape():
    inv=build_artifact_inventory(ROOT); assert inv['artifact_count']==5
def test_flags_false():
    f=governance_flags(); assert f['runtime_authority_granted'] is False and f['provider_dispatch_enabled'] is False
def test_config_false():
    c=json.loads((ROOT/'configs/v1_2/runtime_config_template.json').read_text(encoding='utf-8')); assert c['runtime_authority_granted'] is False and c['provider_dispatch_enabled'] is False
def main():
    tests=[test_readiness_score,test_inventory_shape,test_flags_false,test_config_false]
    for t in tests: run(t.__name__, t)
    print(f'ZANT_LLM_V1_2_STDLIB_TESTS_PASSED=True total={len(tests)}')
    print('RUNTIME_AUTHORITY_GRANTED=False')
    print('PROVIDER_DISPATCH_ENABLED=False')
    return 0
if __name__=='__main__': raise SystemExit(main())
