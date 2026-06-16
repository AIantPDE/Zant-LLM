import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from zant_llm.v0_4_dataset import load_jsonl
from zant_llm.gates import ExplanationAdmissibilityGate,TrainingSampleAdmissibilityGate,FollowUpAdmissibilityGate,CounterfactualAdmissibilityGate,LaneSuccessorAdmissibilityGate
GATES={g.name:g for g in [ExplanationAdmissibilityGate(),TrainingSampleAdmissibilityGate(),FollowUpAdmissibilityGate(),CounterfactualAdmissibilityGate(),LaneSuccessorAdmissibilityGate()]}
def main():
    rows=load_jsonl(ROOT/'data/trace_hix_v0_4/eval_cases_45.jsonl'); passed=0; details=[]
    for row in rows:
        d=GATES[row['gate_name']].evaluate(row); ok=d.decision==row['gate_result']; passed+=int(ok); details.append({'case_id':row['case_id'],'expected':row['gate_result'],'actual':d.decision,'ok':ok})
    report={'report_version':'zant_llm_v0_4_gate_aware_eval_v0','total':len(rows),'passed':passed,'pass_rate':passed/max(1,len(rows)),'runtime_authority_granted':False,'provider_dispatch_enabled':False,'details':details}
    out=ROOT/'reports/v0_4/zant_llm_v0_4_gate_aware_eval_report.json'; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('ZANT_LLM_V0_4_EVALUATED=True'); print('MODE=gate-aware-contract'); print(f'GATE_PASS_RATE={report["pass_rate"]}'); print(f'REPORT={out}'); print('RUNTIME_AUTHORITY_GRANTED=False'); print('PROVIDER_DISPATCH_ENABLED=False'); return 0 if passed==len(rows) else 1
if __name__=='__main__': raise SystemExit(main())

