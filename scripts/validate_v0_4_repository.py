from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def count_jsonl(p: Path) -> int: return sum(1 for line in p.read_text(encoding='utf-8').splitlines() if line.strip())
def main() -> int:
    for rel in ['README.md','GOVERNANCE.md','data/trace_hix_v0_4/train_cases_180.jsonl','data/trace_hix_v0_4/eval_cases_45.jsonl','src/zant_llm/v0_4_dataset.py','scripts/train_v0_4_gemma4_lora.py']:
        assert (ROOT/rel).exists(), f'missing {rel}'
    train=count_jsonl(ROOT/'data/trace_hix_v0_4/train_cases_180.jsonl'); ev=count_jsonl(ROOT/'data/trace_hix_v0_4/eval_cases_45.jsonl')
    assert train==180; assert ev==45
    print('ZANT_LLM_V0_4_REPOSITORY_VALID=True'); print(f'TRAIN_CASES={train}'); print(f'EVAL_CASES={ev}'); print('RUNTIME_AUTHORITY_GRANTED=False'); print('PROVIDER_DISPATCH_ENABLED=False'); return 0
if __name__=='__main__': raise SystemExit(main())

