from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from zant_llm.v0_8_dataset import load_heldout_eval
from zant_llm.gates.heldout_model_eval_gate_v0 import evaluate_heldout_case

def main() -> int:
    rows = load_heldout_eval()
    records=[]; ok=0; counts=Counter()
    for r in rows:
        pred = evaluate_heldout_case(r)
        exp = r['expected_decision']
        passed = pred == exp
        ok += int(passed)
        counts[exp]+=1
        records.append({'id':r['id'],'family':r['family'],'expected':exp,'predicted':pred,'passed':passed})
    pass_rate = ok / len(rows)
    report = {
        'branch':'v0.8-heldout-model-eval',
        'mode':'heldout-contract-eval',
        'heldout_cases':len(rows),
        'pass_rate':pass_rate,
        'decision_counts':dict(counts),
        'records':records,
        'runtime_authority_granted':False,
        'provider_dispatch_enabled':False,
        'successor_recommendation':'READY_TO_V0_8R_MODEL_OUTPUT_AUDIT' if pass_rate>=0.98 else 'BLOCKED_FOR_RESIDUAL_REPAIR'
    }
    out = ROOT/'reports/v0_8/zant_llm_v0_8_heldout_contract_eval_report.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('ZANT_LLM_V0_8_EVALUATED=True')
    print('MODE=heldout-contract-eval')
    print(f'HELDOUT_PASS_RATE={pass_rate}')
    print(f"READY_COUNT={counts.get('READY',0)}")
    print(f"BLOCKED_COUNT={counts.get('BLOCKED',0)}")
    print(f"CLOSEOUT_COUNT={counts.get('CLOSEOUT',0)}")
    print(f"FAILCLOSED_COUNT={counts.get('FAILCLOSED',0)}")
    print(f'REPORT={out}')
    print('RUNTIME_AUTHORITY_GRANTED=False')
    print('PROVIDER_DISPATCH_ENABLED=False')
    return 0 if pass_rate >= 0.98 else 1
if __name__ == '__main__':
    raise SystemExit(main())
