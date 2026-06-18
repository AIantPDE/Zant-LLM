from __future__ import annotations
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from zant_llm.inference_contract_v0_9 import infer_contract

def main():
    data=ROOT/'data/trace_hix_v0_9/inference_contract_cases_160.jsonl'
    out=ROOT/'reports/v0_9/zant_llm_v0_9_inference_contract_eval_report.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    rows=[json.loads(x) for x in data.read_text(encoding='utf-8').splitlines() if x.strip()]
    results=[]; counts={}
    for r in rows:
        pred=infer_contract(r['input'])
        ok=pred['decision']==r['expected'] and pred['runtime_authority_granted'] is False and pred['provider_dispatch_enabled'] is False
        counts[pred['decision']]=counts.get(pred['decision'],0)+1
        results.append({'id':r['id'],'expected':r['expected'],'predicted':pred['decision'],'parse_mode':pred['parse_mode'],'confidence':pred['confidence'],'ok':ok})
    correct=sum(1 for x in results if x['ok'])
    report={'branch':'v0.9-inference-contract-stabilization','mode':'inference-contract-eval','cases':len(rows),'correct':correct,'pass_rate':correct/len(rows),'predicted_counts':counts,'results':results,'runtime_authority_granted':False,'provider_dispatch_enabled':False}
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print('ZANT_LLM_V0_9_EVALUATED=True')
    print('MODE=inference-contract-eval')
    print(f'INFERENCE_CONTRACT_PASS_RATE={report["pass_rate"]}')
    print(f'READY_COUNT={counts.get("READY",0)}')
    print(f'BLOCKED_COUNT={counts.get("BLOCKED",0)}')
    print(f'CLOSEOUT_COUNT={counts.get("CLOSEOUT",0)}')
    print(f'FAILCLOSED_COUNT={counts.get("FAILCLOSED",0)}')
    print(f'REPORT={out}')
    print('RUNTIME_AUTHORITY_GRANTED=False')
    print('PROVIDER_DISPATCH_ENABLED=False')
if __name__=='__main__': main()
