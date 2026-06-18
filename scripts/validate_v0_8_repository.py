from __future__ import annotations
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def count_jsonl(p: Path) -> int:
    return sum(1 for line in p.open('r', encoding='utf-8') if line.strip())

def main() -> int:
    required = [
        'README.md','GOVERNANCE.md','data/trace_hix_v0_8/heldout_eval_180.jsonl',
        'data/trace_hix_v0_8/heldout_smoke_45.jsonl','scripts/eval_v0_8_heldout_contract.py',
        'scripts/eval_v0_8_heldout_model.py','src/zant_llm/gates/heldout_model_eval_gate_v0.py'
    ]
    for rel in required:
        if not (ROOT / rel).exists():
            raise SystemExit(f'Missing required file: {rel}')
    eval_count = count_jsonl(ROOT/'data/trace_hix_v0_8/heldout_eval_180.jsonl')
    smoke_count = count_jsonl(ROOT/'data/trace_hix_v0_8/heldout_smoke_45.jsonl')
    assert eval_count == 180, eval_count
    assert smoke_count == 45, smoke_count
    print('ZANT_LLM_V0_8_REPOSITORY_VALID=True')
    print(f'HELDOUT_CASES={eval_count}')
    print(f'SMOKE_CASES={smoke_count}')
    print('RUNTIME_AUTHORITY_GRANTED=False')
    print('PROVIDER_DISPATCH_ENABLED=False')
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
