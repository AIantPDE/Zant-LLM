from __future__ import annotations
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from zant_llm.gates import evaluate_realworld_case

def load_jsonl(path):
    return [json.loads(line) for line in Path(path).read_text(encoding='utf-8').splitlines() if line.strip()]

def main():
    data_path = ROOT/'data/trace_hix_v0_6/realworld_eval_300.jsonl'
    rows = load_jsonl(data_path)
    results=[]; counts={}; failed=[]
    for row in rows:
        pred=evaluate_realworld_case(row)
        actual=pred['decision']; exp=row['expected_decision']
        ok=actual==exp
        counts[actual]=counts.get(actual,0)+1
        item={'id':row['id'],'family':row['family'],'expected':exp,'actual':actual,'ok':ok,'reason':pred['reason']}
        results.append(item)
        if not ok: failed.append(item)
    report={
        'report_version':'zant_llm_v0_6_realworld_adversarial_eval_report_v0',
        'mode':'realworld-adversarial-eval',
        'total':len(rows),'passed':len(rows)-len(failed),'failed':len(failed),
        'pass_rate':(len(rows)-len(failed))/len(rows),
        'decision_counts':counts,
        'runtime_authority_granted':False,
        'provider_dispatch_enabled':False,
        'failed_items':failed[:20],
        'results':results,
    }
    out=ROOT/'reports/v0_6/zant_llm_v0_6_realworld_eval_report.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('ZANT_LLM_V0_6_EVALUATED=True')
    print('MODE=realworld-adversarial-eval')
    print(f'REALWORLD_ADV_PASS_RATE={report["pass_rate"]}')
    for k in ['READY','BLOCKED','CLOSEOUT','FAILCLOSED']:
        print(f'{k}_COUNT={counts.get(k,0)}')
    print(f'REPORT={out}')
    print('RUNTIME_AUTHORITY_GRANTED=False')
    print('PROVIDER_DISPATCH_ENABLED=False')
    return 0 if not failed else 1
if __name__=='__main__': raise SystemExit(main())
