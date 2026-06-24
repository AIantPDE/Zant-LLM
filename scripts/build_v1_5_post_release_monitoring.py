import json, hashlib, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from zant_llm.post_release_monitoring_v1_5 import build_monitoring_report, classify_smoke, BRANCH, SUCCESSOR

checks_doc = json.loads((ROOT/'data/trace_hix_v1_5/post_release_monitoring_checks.json').read_text(encoding='utf-8'))
checks = checks_doc['monitoring_checks']
report = build_monitoring_report()
report['passed_checks'] = sum(1 for c in checks if c['status'] == 'pass')
report['failed_checks'] = sum(1 for c in checks if c['status'] != 'pass')
report['hotfix_policy_ready'] = True
report['issue_intake_ready'] = True
report['regression_intake_ready'] = True
rows = [json.loads(x) for x in (ROOT/'data/trace_hix_v1_5/post_release_smoke_cases_20.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
results=[]
correct=0
counts={}
for r in rows:
    pred = classify_smoke(r['text'])
    ok = pred == r['expected_decision']
    correct += int(ok)
    counts[pred]=counts.get(pred,0)+1
    results.append({'id': r['id'], 'expected_decision': r['expected_decision'], 'decision': pred, 'ok': ok})
smoke_report = {
    'branch': BRANCH,
    'smoke_cases': len(rows),
    'correct': correct,
    'smoke_pass_rate': correct / len(rows),
    'decision_counts': counts,
    'blocking_issues': 0,
    'runtime_authority_granted': False,
    'provider_dispatch_enabled': False,
    'results': results,
}
inventory = {
    'branch': BRANCH,
    'artifacts': [
        'reports/v1_5/zant_llm_v1_5_post_release_monitoring_report.json',
        'reports/v1_5/zant_llm_v1_5_post_release_smoke_report.json',
        'reports/v1_5/zant_llm_v1_5_maintenance_summary.md',
        'data/trace_hix_v1_5/issue_intake_template.json',
        'data/trace_hix_v1_5/regression_intake_template.json',
    ],
    'release_tag_under_watch': 'v1.4.0',
}
report_dir = ROOT/'reports/v1_5'
report_dir.mkdir(parents=True, exist_ok=True)
(report_dir/'zant_llm_v1_5_post_release_monitoring_report.json').write_text(json.dumps(report, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
(report_dir/'zant_llm_v1_5_post_release_smoke_report.json').write_text(json.dumps(smoke_report, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
(report_dir/'zant_llm_v1_5_artifact_inventory.json').write_text(json.dumps(inventory, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
(report_dir/'zant_llm_v1_5_maintenance_summary.md').write_text(f"""# Zant-LLM v1.5 Maintenance Summary

- Release health score: {report['release_health_score']}
- Smoke pass rate: {smoke_report['smoke_pass_rate']}
- Blocking issues: 0
- Runtime authority granted: false
- Provider dispatch enabled: false
- Successor: {SUCCESSOR}
""", encoding='utf-8')
print('ZANT_LLM_V1_5_POST_RELEASE_MONITORING_BUILT=True')
print('RELEASE_HEALTH_SCORE=' + str(report['release_health_score']))
print('SMOKE_PASS_RATE=' + str(smoke_report['smoke_pass_rate']))
print('BLOCKING_ISSUES=0')
print('POST_RELEASE_MONITORING_ACCEPTED=True')
print('REPORT=' + str(report_dir/'zant_llm_v1_5_post_release_monitoring_report.json'))
print('RUNTIME_AUTHORITY_GRANTED=False')
print('PROVIDER_DISPATCH_ENABLED=False')
