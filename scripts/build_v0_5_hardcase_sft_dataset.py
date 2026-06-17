import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from zant_llm.v0_5_dataset import read_jsonl, make_sft_row
def w(p,rows):
    Path(p).write_text('\n'.join(json.dumps(r,ensure_ascii=False,sort_keys=True) for r in rows)+'\n',encoding='utf-8')
def main():
    tr=[make_sft_row(c) for c in read_jsonl(ROOT/'data/trace_hix_v0_5/hard_train_240.jsonl')]
    ev=[make_sft_row(c) for c in read_jsonl(ROOT/'data/trace_hix_v0_5/hard_eval_60.jsonl')]
    w(ROOT/'data/trace_hix_v0_5/sft_train_240.jsonl',tr); w(ROOT/'data/trace_hix_v0_5/sft_eval_60.jsonl',ev)
    print('ZANT_LLM_V0_5_SFT_DATASET_BUILT=True'); print(f'SFT_TRAIN_COUNT={len(tr)}'); print(f'SFT_EVAL_COUNT={len(ev)}')
if __name__=='__main__': main()
