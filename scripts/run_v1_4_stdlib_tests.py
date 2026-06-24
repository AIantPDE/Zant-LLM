from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from zant_llm.final_release_v1_4 import build_final_release_report, tag_recommendation, RECOMMENDED_TAG
from zant_llm.governance import runtime_flags
checks=json.loads((ROOT/'data/trace_hix_v1_4/final_release_checks.json').read_text(encoding='utf-8'))
report=build_final_release_report(checks)
assert report['final_release_score']==1.0; print('PASS test_final_release_score')
assert report['blocking_issues']==0; print('PASS test_blocking_zero')
assert report['final_release_accepted'] is True; print('PASS test_final_release_accepted')
assert tag_recommendation()['recommended_tag']==RECOMMENDED_TAG; print('PASS test_tag_recommendation')
flags=runtime_flags(); assert flags['runtime_authority_granted'] is False and flags['provider_dispatch_enabled'] is False; print('PASS test_flags_false')
print('ZANT_LLM_V1_4_STDLIB_TESTS_PASSED=True total=5')
print('RUNTIME_AUTHORITY_GRANTED=False')
print('PROVIDER_DISPATCH_ENABLED=False')
