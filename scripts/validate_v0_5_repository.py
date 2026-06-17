from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def count(p): return sum(1 for x in Path(p).read_text(encoding='utf-8').splitlines() if x.strip())
def main():
    for r in ['README.md','GOVERNANCE.md','data/trace_hix_v0_5/hard_train_240.jsonl','data/trace_hix_v0_5/hard_eval_60.jsonl','src/zant_llm/gates/hardcase_failclosed_gate_v0.py','scripts/eval_v0_5_failclosed_hard_cases.py']:
        if not (ROOT/r).exists(): raise SystemExit(f'Missing required file: {r}')
    tr=count(ROOT/'data/trace_hix_v0_5/hard_train_240.jsonl'); ev=count(ROOT/'data/trace_hix_v0_5/hard_eval_60.jsonl')
    assert tr==240; assert ev==60
    print('ZANT_LLM_V0_5_REPOSITORY_VALID=True'); print(f'TRAIN_CASES={tr}'); print(f'EVAL_CASES={ev}'); print('RUNTIME_AUTHORITY_GRANTED=False'); print('PROVIDER_DISPATCH_ENABLED=False')
if __name__=='__main__': main()
