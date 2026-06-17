from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
# dataset is prebuilt; validate counts
for name, expected in [('sft_train_360.jsonl',360),('sft_eval_90.jsonl',90)]:
    path=ROOT/'data/trace_hix_v0_7'/name
    count=sum(1 for line in path.open(encoding='utf-8') if line.strip())
    if count!=expected: raise SystemExit(f'{name} count mismatch: {count}')
print('ZANT_LLM_V0_7_SFT_DATASET_BUILT=True')
print('SFT_TRAIN_COUNT=360')
print('SFT_EVAL_COUNT=90')
