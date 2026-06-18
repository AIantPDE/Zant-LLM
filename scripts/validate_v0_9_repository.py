from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    'README.md','GOVERNANCE.md','src/zant_llm/inference_contract_v0_9.py',
    'scripts/cli_infer_v0_9.py','scripts/api_server_v0_9.py',
    'scripts/eval_v0_9_inference_contract.py','data/trace_hix_v0_9/inference_contract_cases_160.jsonl'
]

def main() -> int:
    for r in REQUIRED:
        p=ROOT/r
        if not p.exists():
            raise AssertionError(f'missing required file: {r}')
    cases = [json.loads(x) for x in (ROOT/'data/trace_hix_v0_9/inference_contract_cases_160.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
    smoke = [json.loads(x) for x in (ROOT/'data/trace_hix_v0_9/smoke_cases_40.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
    assert len(cases)==160, len(cases)
    assert len(smoke)==40, len(smoke)
    text='\n'.join(p.read_text(encoding='utf-8', errors='ignore') for p in (ROOT/'src').rglob('*.py'))
    if 'runtime_authority_granted = True' in text or 'provider_dispatch_enabled = True' in text:
        raise AssertionError('forbidden runtime/provider grant found')
    print('ZANT_LLM_V0_9_REPOSITORY_VALID=True')
    print('INFERENCE_CASES=160')
    print('SMOKE_CASES=40')
    print('RUNTIME_AUTHORITY_GRANTED=False')
    print('PROVIDER_DISPATCH_ENABLED=False')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
