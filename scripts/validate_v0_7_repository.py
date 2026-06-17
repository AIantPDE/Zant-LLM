from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
REQ=[
 'data/trace_hix_v0_7/calibration_train_360.jsonl','data/trace_hix_v0_7/calibration_eval_90.jsonl',
 'data/trace_hix_v0_7/sft_train_360.jsonl','data/trace_hix_v0_7/sft_eval_90.jsonl',
 'src/zant_llm/gates/calibration_sft_gate_v0.py','scripts/run_v0_7_stdlib_tests.py',
 'scripts/eval_v0_7_calibration_sft_contract.py','scripts/train_v0_7_gemma4_lora.py']
for p in REQ:
    if not (ROOT/p).exists(): raise SystemExit(f'Missing required file: {p}')
def count(path):
    return sum(1 for line in (ROOT/path).open('r',encoding='utf-8') if line.strip())
tr=count('data/trace_hix_v0_7/calibration_train_360.jsonl'); ev=count('data/trace_hix_v0_7/calibration_eval_90.jsonl')
assert tr==360, tr; assert ev==90, ev
print('ZANT_LLM_V0_7_REPOSITORY_VALID=True')
print(f'TRAIN_CASES={tr}')
print(f'EVAL_CASES={ev}')
print('RUNTIME_AUTHORITY_GRANTED=False')
print('PROVIDER_DISPATCH_ENABLED=False')
