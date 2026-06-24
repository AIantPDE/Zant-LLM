from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[1]
REQ = [
    'src/zant_llm/post_release_monitoring_v1_5.py',
    'data/trace_hix_v1_5/post_release_monitoring_checks.json',
    'data/trace_hix_v1_5/post_release_smoke_cases_20.jsonl',
    'scripts/build_v1_5_post_release_monitoring.py',
]
missing = [p for p in REQ if not (ROOT / p).exists()]
if missing:
    raise SystemExit('missing required files: ' + ', '.join(missing))
checks = json.loads((ROOT / 'data/trace_hix_v1_5/post_release_monitoring_checks.json').read_text(encoding='utf-8'))['monitoring_checks']
smoke = [x for x in (ROOT / 'data/trace_hix_v1_5/post_release_smoke_cases_20.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
print('[Zant-LLM v1.5] repository root:', ROOT)
print('ZANT_LLM_V1_5_REPOSITORY_VALID=True')
print('MONITORING_CHECKS=' + str(len(checks)))
print('SMOKE_CASES=' + str(len(smoke)))
print('RUNTIME_AUTHORITY_GRANTED=False')
print('PROVIDER_DISPATCH_ENABLED=False')
