from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[1]
REQ = [
    'src/zant_llm/final_archive_v1_4r.py',
    'data/trace_hix_v1_4R/archive_checks.json',
    'data/trace_hix_v1_4R/final_smoke_cases_16.jsonl',
    'scripts/build_v1_4R_final_smoke_and_archive.py',
]
missing = [p for p in REQ if not (ROOT / p).exists()]
if missing:
    raise SystemExit('missing required files: ' + ', '.join(missing))
checks = json.loads((ROOT / 'data/trace_hix_v1_4R/archive_checks.json').read_text(encoding='utf-8'))['archive_checks']
smoke = [x for x in (ROOT / 'data/trace_hix_v1_4R/final_smoke_cases_16.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
print('[Zant-LLM v1.4R] repository root:', ROOT)
print('ZANT_LLM_V1_4R_REPOSITORY_VALID=True')
print('ARCHIVE_CHECKS=' + str(len(checks)))
print('SMOKE_CASES=' + str(len(smoke)))
print('RUNTIME_AUTHORITY_GRANTED=False')
print('PROVIDER_DISPATCH_ENABLED=False')
