from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
 'README.md','GOVERNANCE.md','VERSION',
 'data/trace_hix_v0_6/realworld_eval_300.jsonl',
 'data/trace_hix_v0_6/realworld_smoke_60.jsonl',
 'scripts/eval_v0_6_realworld_adversarial.py',
 'src/zant_llm/gates/realworld_adversarial_gate_v0.py',
]

def load_jsonl(path):
    return [json.loads(line) for line in Path(path).read_text(encoding='utf-8').splitlines() if line.strip()]

def main():
    for rel in REQUIRED:
        p=ROOT/rel
        if not p.exists(): raise SystemExit(f'Missing required file: {rel}')
    rows=load_jsonl(ROOT/'data/trace_hix_v0_6/realworld_eval_300.jsonl')
    if len(rows)!=300: raise SystemExit(f'Expected 300 eval cases, got {len(rows)}')
    smoke=load_jsonl(ROOT/'data/trace_hix_v0_6/realworld_smoke_60.jsonl')
    if len(smoke)!=60: raise SystemExit(f'Expected 60 smoke cases, got {len(smoke)}')
    print('ZANT_LLM_V0_6_REPOSITORY_VALID=True')
    print(f'EVAL_CASES={len(rows)}')
    print(f'SMOKE_CASES={len(smoke)}')
    print('RUNTIME_AUTHORITY_GRANTED=False')
    print('PROVIDER_DISPATCH_ENABLED=False')
    return 0
if __name__=='__main__': raise SystemExit(main())
