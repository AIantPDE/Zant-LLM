import argparse, json, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from zant_llm.inference_contract_v0_10 import batch_infer

def load_jsonl(p):
    return [json.loads(line) for line in open(p,encoding='utf-8') if line.strip()]
def write_jsonl(p, rows):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True)
    with open(p,'w',encoding='utf-8') as f:
        for r in rows: f.write(json.dumps(r,ensure_ascii=False)+'\n')
ap=argparse.ArgumentParser()
ap.add_argument('--input', default=str(ROOT/'data/trace_hix_v0_10/sample_batch_input.jsonl'))
ap.add_argument('--output', default=str(ROOT/'outputs/v0_10/batch_infer_output.jsonl'))
args=ap.parse_args()
rows=load_jsonl(args.input)
res=batch_infer(rows)
write_jsonl(args.output,res)
report={'branch':'v0.10-runtime-api-batch-harness','mode':'batch-infer','input':args.input,'output':args.output,'count':len(res),'runtime_authority_granted':False,'provider_dispatch_enabled':False,'ts_unix':time.time()}
out=ROOT/'reports/v0_10/zant_llm_v0_10_batch_infer_report.json'; out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('ZANT_LLM_V0_10_BATCH_INFER_OK=True')
print('COUNT='+str(len(res)))
print('OUTPUT='+args.output)
print('RUNTIME_AUTHORITY_GRANTED=False')
print('PROVIDER_DISPATCH_ENABLED=False')
