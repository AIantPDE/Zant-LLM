import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from zant_llm.inference_contract_v0_10 import batch_infer

def load_jsonl(p):
    return [json.loads(line) for line in open(p,encoding='utf-8') if line.strip()]
def main():
    data=load_jsonl(ROOT/'data/trace_hix_v0_10/batch_eval_cases_200.jsonl')
    results=batch_infer(data)
    total=len(results); correct=sum(1 for r in results if r.get('ok'))
    counts={d:sum(1 for r in results if r['decision']==d) for d in ['READY','BLOCKED','CLOSEOUT','FAILCLOSED']}
    report={'branch':'v0.10-runtime-api-batch-harness','mode':'runtime-api-batch-harness-eval','total':total,'correct':correct,'pass_rate':correct/total if total else 0,'counts':counts,'results':results,'runtime_authority_granted':False,'provider_dispatch_enabled':False}
    out=ROOT/'reports/v0_10/zant_llm_v0_10_batch_harness_eval_report.json'; out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('ZANT_LLM_V0_10_EVALUATED=True')
    print('MODE=runtime-api-batch-harness-eval')
    print(f'BATCH_HARNESS_PASS_RATE={report["pass_rate"]}')
    print(f'READY_COUNT={counts["READY"]}')
    print(f'BLOCKED_COUNT={counts["BLOCKED"]}')
    print(f'CLOSEOUT_COUNT={counts["CLOSEOUT"]}')
    print(f'FAILCLOSED_COUNT={counts["FAILCLOSED"]}')
    print('REPORT='+str(out))
    print('RUNTIME_AUTHORITY_GRANTED=False')
    print('PROVIDER_DISPATCH_ENABLED=False')
if __name__=='__main__': main()
