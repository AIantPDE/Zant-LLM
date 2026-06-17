from pathlib import Path
import json, sys
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from zant_llm.gates.calibration_sft_gate_v0 import CalibrationSFTGate
cases=[json.loads(l) for l in (ROOT/'data/trace_hix_v0_7/calibration_eval_90.jsonl').open(encoding='utf-8') if l.strip()]
passed=0; cnt=Counter()
for c in cases:
    d=CalibrationSFTGate().evaluate(c)
    cnt[d.decision]+=1
    passed += int(d.decision==c['expected_decision'])
report={'report_version':'zant_llm_v0_7_calibration_contract_eval_v1','mode':'calibration-informed-sft-contract','total':len(cases),'pass_rate':passed/len(cases),'decision_counts':dict(cnt),'runtime_authority_granted':False,'provider_dispatch_enabled':False}
out=ROOT/'reports/v0_7/zant_llm_v0_7_calibration_sft_eval_report.json'
out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('ZANT_LLM_V0_7_EVALUATED=True')
print('MODE=calibration-informed-sft-contract')
print(f'CALIBRATION_SFT_PASS_RATE={report["pass_rate"]}')
for k in ['READY','BLOCKED','CLOSEOUT','FAILCLOSED']:
    print(f'{k}_COUNT={cnt.get(k,0)}')
print(f'REPORT={out}')
print('RUNTIME_AUTHORITY_GRANTED=False')
print('PROVIDER_DISPATCH_ENABLED=False')
