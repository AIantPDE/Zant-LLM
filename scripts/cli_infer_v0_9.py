from __future__ import annotations
import argparse, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from zant_llm.inference_contract_v0_9 import infer_contract

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--text', default='')
    ap.add_argument('--model-output', default=None)
    ap.add_argument('--input-jsonl')
    ap.add_argument('--output-jsonl')
    args=ap.parse_args()
    if args.input_jsonl:
        out=[]
        for line in Path(args.input_jsonl).read_text(encoding='utf-8').splitlines():
            if not line.strip(): continue
            obj=json.loads(line)
            res=infer_contract(obj.get('input',''), obj.get('model_output'))
            res['id']=obj.get('id')
            out.append(res)
        text=''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in out)
        if args.output_jsonl:
            Path(args.output_jsonl).parent.mkdir(parents=True, exist_ok=True)
            Path(args.output_jsonl).write_text(text, encoding='utf-8')
        else:
            print(text, end='')
    else:
        print(json.dumps(infer_contract(args.text, args.model_output), ensure_ascii=False))
if __name__=='__main__': main()
