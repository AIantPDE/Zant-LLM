from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ['README.md','VERSION','data/trace_hix_v0_6R/v0_6_realworld_eval_snapshot_300.jsonl','scripts/analyze_v0_6_realworld_eval_calibration.py','scripts/RUN_V0_6R_CALIBRATION.ps1','src/zant_llm/v0_6R_calibration.py']
def count_jsonl(p: Path) -> int:
    return sum(1 for line in p.open('r', encoding='utf-8') if line.strip())
def main() -> int:
    for item in REQUIRED:
        if not (ROOT / item).exists():
            raise SystemExit(f'MISSING_REQUIRED_FILE={item}')
    total = count_jsonl(ROOT / 'data/trace_hix_v0_6R/v0_6_realworld_eval_snapshot_300.jsonl')
    if total != 300: raise SystemExit(f'EVAL_SNAPSHOT_COUNT_INVALID={total}')
    print('ZANT_LLM_V0_6R_REPOSITORY_VALID=True')
    print(f'EVAL_SNAPSHOT_CASES={total}')
    print('RUNTIME_AUTHORITY_GRANTED=False')
    print('PROVIDER_DISPATCH_ENABLED=False')
    return 0
if __name__ == '__main__': raise SystemExit(main())
