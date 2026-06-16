import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from zant_llm.v0_4_dataset import load_jsonl, to_sft
def write(src,dst):
    rows=load_jsonl(src)
    with dst.open('w',encoding='utf-8') as f:
        for r in rows: f.write(json.dumps(to_sft(r),ensure_ascii=False)+'\n')
    return len(rows)
def main():
    n1=write(ROOT/'data/trace_hix_v0_4/train_cases_180.jsonl',ROOT/'data/trace_hix_v0_4/sft_train_180.jsonl'); n2=write(ROOT/'data/trace_hix_v0_4/eval_cases_45.jsonl',ROOT/'data/trace_hix_v0_4/sft_eval_45.jsonl')
    print('ZANT_LLM_V0_4_SFT_DATASET_BUILT=True'); print(f'SFT_TRAIN_COUNT={n1}'); print(f'SFT_EVAL_COUNT={n2}'); return 0
if __name__=='__main__': raise SystemExit(main())

