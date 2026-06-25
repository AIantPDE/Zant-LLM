from pathlib import Path
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / 'reports' / 'v1_6'
REPORT_DIR.mkdir(parents=True, exist_ok=True)
MOD = ROOT / 'src' / 'zant_llm' / 'runtime_observability_v1_6.py'
spec = importlib.util.spec_from_file_location('runtime_observability_v1_6', MOD)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

observability = mod.build_runtime_observability_report(ROOT)
dashboard = mod.build_dashboard_report(ROOT, observability)
operator = {
    'version': 'v1.6',
    'branch': observability['branch'],
    'operator_daily_cases': observability['operator_daily_cases'],
    'operator_daily_pass_rate': observability['operator_daily_pass_rate'],
    'blocking_issues': observability['blocking_issues'],
    'runtime_authority_granted': False,
    'provider_dispatch_enabled': False,
}
inventory = {
    'version': 'v1.6',
    'branch': observability['branch'],
    'artifact_groups': ['data','docs','schemas','registries','reports','scripts','src'],
    'required_reports': [
        'zant_llm_v1_6_observability_report.json',
        'zant_llm_v1_6_dashboard_report.json',
        'zant_llm_v1_6_operator_daily_report.json',
    ],
}
summary = f"""# Zant-LLM v1.6 observability summary

- Runtime health score: {observability['runtime_health_score']}
- Dashboard completeness score: {observability['dashboard_completeness_score']}
- Operator daily pass rate: {observability['operator_daily_pass_rate']}
- Regression pass rate: {observability['regression_pass_rate']}
- Blocking issues: {observability['blocking_issues']}
- Dashboard ready: {observability['dashboard_ready']}
- Runtime authority granted: False
- Provider dispatch enabled: False
"""

def write_json(name, obj):
    (REPORT_DIR / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

write_json('zant_llm_v1_6_observability_report.json', observability)
write_json('zant_llm_v1_6_dashboard_report.json', dashboard)
write_json('zant_llm_v1_6_operator_daily_report.json', operator)
write_json('zant_llm_v1_6_artifact_inventory.json', inventory)
(REPORT_DIR / 'zant_llm_v1_6_observability_summary.md').write_text(summary, encoding='utf-8')

print('ZANT_LLM_V1_6_OBSERVABILITY_BUILT=True')
print(f"RUNTIME_HEALTH_SCORE={observability['runtime_health_score']}")
print(f"DASHBOARD_COMPLETENESS_SCORE={observability['dashboard_completeness_score']}")
print(f"OPERATOR_DAILY_PASS_RATE={observability['operator_daily_pass_rate']}")
print(f"REGRESSION_PASS_RATE={observability['regression_pass_rate']}")
print(f"BLOCKING_ISSUES={observability['blocking_issues']}")
print(f"DASHBOARD_READY={observability['dashboard_ready']}")
print(f"REPORT={REPORT_DIR / 'zant_llm_v1_6_observability_report.json'}")
print('RUNTIME_AUTHORITY_GRANTED=False')
print('PROVIDER_DISPATCH_ENABLED=False')
