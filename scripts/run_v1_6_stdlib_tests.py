from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / 'src' / 'zant_llm' / 'runtime_observability_v1_6.py'
spec = importlib.util.spec_from_file_location('runtime_observability_v1_6', MOD)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

report = mod.build_runtime_observability_report(ROOT)
dashboard = mod.build_dashboard_report(ROOT, report)

def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print('PASS ' + name)

check('test_runtime_health_score', report['runtime_health_score'] == 1.0)
check('test_dashboard_completeness_score', report['dashboard_completeness_score'] == 1.0)
check('test_operator_daily_pass_rate', report['operator_daily_pass_rate'] == 1.0)
check('test_regression_pass_rate', report['regression_pass_rate'] == 1.0)
check('test_blocking_zero', report['blocking_issues'] == 0)
check('test_dashboard_ready', report['dashboard_ready'] is True)
check('test_dashboard_read_only', dashboard['read_only'] is True)
check('test_panels_count', dashboard['panels_total'] == 12)
check('test_flags_false', report['runtime_authority_granted'] is False and report['provider_dispatch_enabled'] is False)
print('ZANT_LLM_V1_6_STDLIB_TESTS_PASSED=True total=9')
print('RUNTIME_AUTHORITY_GRANTED=False')
print('PROVIDER_DISPATCH_ENABLED=False')
