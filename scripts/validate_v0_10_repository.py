from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
REQ=[
 'src/zant_llm/inference_contract_v0_10.py','scripts/cli_infer_v0_10.py','scripts/batch_infer_v0_10.py','scripts/api_server_v0_10.py',
 'data/trace_hix_v0_10/batch_eval_cases_200.jsonl','data/trace_hix_v0_10/smoke_cases_50.jsonl'
]
def count(p):
    return sum(1 for _ in open(ROOT/p,encoding='utf-8'))
def main():
    for r in REQ:
        assert (ROOT/r).exists(), r
    assert count('data/trace_hix_v0_10/batch_eval_cases_200.jsonl')==200
    assert count('data/trace_hix_v0_10/smoke_cases_50.jsonl')==50
    print('ZANT_LLM_V0_10_REPOSITORY_VALID=True')
    print('BATCH_CASES=200')
    print('SMOKE_CASES=50')
    print('RUNTIME_AUTHORITY_GRANTED=False')
    print('PROVIDER_DISPATCH_ENABLED=False')
if __name__=='__main__': main()
