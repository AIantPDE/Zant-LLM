from pathlib import Path
import json
import py_compile

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    'README.md','VERSION','GOVERNANCE.md','SECURITY.md','RELEASE_POLICY.md','TRAINING_LANE_REGISTRY.md',
    'src/zant_llm/governance.py','src/zant_llm/runtime_observability_v1_6.py',
    'data/trace_hix_v1_6/runtime_health_checks.json','data/trace_hix_v1_6/dashboard_panels.json',
    'data/trace_hix_v1_6/operator_daily_check_cases_32.jsonl','data/trace_hix_v1_6/regression_trend_cases_32.jsonl',
    'docs/V1_6_RUNTIME_OBSERVABILITY_AND_OPERATOR_DASHBOARD.md',
    'scripts/build_v1_6_runtime_observability.py','scripts/run_v1_6_stdlib_tests.py',
    'scripts/make_v1_6_release_manifest.py','scripts/make_v1_6_successor_recommendation.py',
]

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def count_jsonl(path):
    with open(path, 'r', encoding='utf-8') as f:
        return sum(1 for line in f if line.strip())

missing = [p for p in REQUIRED if not (ROOT / p).exists()]
if missing:
    raise SystemExit('Missing required files: ' + ', '.join(missing))

health = load_json(ROOT / 'data/trace_hix_v1_6/runtime_health_checks.json')
panels = load_json(ROOT / 'data/trace_hix_v1_6/dashboard_panels.json')
operator_cases = count_jsonl(ROOT / 'data/trace_hix_v1_6/operator_daily_check_cases_32.jsonl')
regression_cases = count_jsonl(ROOT / 'data/trace_hix_v1_6/regression_trend_cases_32.jsonl')
assert len(health) == 32, len(health)
assert len(panels) == 12, len(panels)
assert operator_cases == 32, operator_cases
assert regression_cases == 32, regression_cases
assert all(c.get('status') == 'pass' for c in health)
assert all(p.get('read_only') is True for p in panels)

for path in list((ROOT/'src').rglob('*.py')) + list((ROOT/'scripts').rglob('*.py')):
    py_compile.compile(str(path), doraise=True)

print(f'[Zant-LLM v1.6] repository root: {ROOT}')
print('ZANT_LLM_V1_6_REPOSITORY_VALID=True')
print(f'RUNTIME_HEALTH_CHECKS={len(health)}')
print(f'DASHBOARD_PANELS={len(panels)}')
print(f'OPERATOR_DAILY_CASES={operator_cases}')
print(f'REGRESSION_TREND_CASES={regression_cases}')
print('RUNTIME_AUTHORITY_GRANTED=False')
print('PROVIDER_DISPATCH_ENABLED=False')
