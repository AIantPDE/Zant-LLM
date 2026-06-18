from __future__ import annotations
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from zant_llm.output_calibration_v0_8R import calibrate_output, slice_generated_tokens
from zant_llm.governance import assert_governance
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--base-model",default=r"E:\gemma-4-E2B-it")
    ap.add_argument("--adapter-path",default=r"C:\Users\Administrator\Desktop\Zant-LLM-v0.7-push-work\outputs\v0_7\gemma4_lora_adapter")
    ap.add_argument("--cases",default=str(ROOT/"data/trace_hix_v0_8R/calibration_probe_cases_12.jsonl"))
    ap.add_argument("--max-cases",type=int,default=12)
    ap.add_argument("--dry-run",action="store_true")
    ap.add_argument("--output",default=str(ROOT/"reports/v0_8R/zant_llm_v0_8R_live_calibrated_model_probe_report.json"))
    args=ap.parse_args(); assert_governance()
    cases=[json.loads(x) for x in Path(args.cases).read_text(encoding="utf-8").splitlines() if x.strip()][:args.max_cases]
    results=[]
    if args.dry_run:
        for r in cases:
            d=calibrate_output(r.get("raw_output",""),r.get("case_text",""))
            results.append({"id":r["id"],"expected":r["expected"],"predicted":d.predicted,"parse_mode":d.parse_mode,"ok":d.predicted==r["expected"]})
    else:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from peft import PeftModel
        model=AutoModelForCausalLM.from_pretrained(args.base_model,trust_remote_code=True,torch_dtype=torch.float32,local_files_only=True)
        model=PeftModel.from_pretrained(model,args.adapter_path,local_files_only=True)
        tok=AutoTokenizer.from_pretrained(args.adapter_path,trust_remote_code=True,local_files_only=True)
        model.eval()
        for r in cases:
            prompt='Classify this heldout input as READY, BLOCKED, CLOSEOUT, or FAILCLOSED. Return compact JSON only, e.g. {"decision":"BLOCKED"}.\n'+r["case_text"]
            inputs=tok(prompt,return_tensors="pt")
            with torch.no_grad():
                out_ids=model.generate(**inputs,max_new_tokens=32,do_sample=False,pad_token_id=tok.eos_token_id,eos_token_id=tok.eos_token_id)
            new_text=slice_generated_tokens(tok,inputs["input_ids"],out_ids)
            d=calibrate_output(new_text,r.get("case_text",""))
            results.append({"id":r["id"],"expected":r["expected"],"raw_new_output":new_text,"predicted":d.predicted,"parse_mode":d.parse_mode,"confidence":d.confidence,"ok":d.predicted==r["expected"]})
    report={"branch":"v0.8R-heldout-model-output-calibration","mode":"live-calibrated-model-probe"+("-dry-run" if args.dry_run else ""),"cases":len(results),"correct":sum(1 for r in results if r["ok"]),"calibrated_accuracy":(sum(1 for r in results if r["ok"])/len(results) if results else 0.0),"results":results,"runtime_authority_granted":False,"provider_dispatch_enabled":False}
    out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("ZANT_LLM_V0_8R_LIVE_MODEL_PROBE_OK=True"); print(f"CASES={len(results)}"); print(f"REPORT={out}"); print("RUNTIME_AUTHORITY_GRANTED=False"); print("PROVIDER_DISPATCH_ENABLED=False")
if __name__=="__main__": main()
