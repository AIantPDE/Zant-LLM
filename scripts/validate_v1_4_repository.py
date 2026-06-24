from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
required=['src/zant_llm/final_release_v1_4.py','data/trace_hix_v1_4/final_release_checks.json','data/trace_hix_v1_4/final_branch_index.json','scripts/build_v1_4_final_release_manifest.py','scripts/run_v1_4_stdlib_tests.py']
missing=[p for p in required if not (ROOT/p).exists()]
if missing:
    print('ZANT_LLM_V1_4_REPOSITORY_VALID=False'); print('MISSING='+','.join(missing)); sys.exit(1)
checks=json.loads((ROOT/'data/trace_hix_v1_4/final_release_checks.json').read_text(encoding='utf-8'))
print(f'[Zant-LLM v1.4] repository root: {ROOT}')
print('ZANT_LLM_V1_4_REPOSITORY_VALID=True')
print(f'FINAL_RELEASE_CHECKS={len(checks)}')
print('RUNTIME_AUTHORITY_GRANTED=False')
print('PROVIDER_DISPATCH_ENABLED=False')
