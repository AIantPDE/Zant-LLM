from __future__ import annotations
import argparse,json,sys
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from zant_llm.output_calibration_v0_8R import calibrate_output
from zant_llm.governance import assert_governance
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",default=str(ROOT/"data/trace_hix_v0_8R/calibration_probe_cases_12.jsonl"))
    ap.add_argument("--output",default=str(ROOT/"reports/v0_8R/zant_llm_v0_8R_calibrated_model_probe_report.json"))
    args=ap.parse_args(); assert_governance()
    rows=[]; counts=Counter(); modes=Counter(); correct=0; total=0
    for line in Path(args.input).read_text(encoding="utf-8").splitlines():
        if not line.strip(): continue
        r=json.loads(line); dec=calibrate_output(r.get("raw_output",""),r.get("case_text",""))
        ok=dec.predicted==r["expected"]; correct+=int(ok); total+=1
        counts[dec.predicted]+=1; modes[dec.parse_mode]+=1
        rows.append({"id":r["id"],"expected":r["expected"],"predicted":dec.predicted,"ok":ok,"parse_mode":dec.parse_mode,"confidence":dec.confidence,"reason":dec.reason})
    acc=correct/total if total else 0.0
    report={"branch":"v0.8R-heldout-model-output-calibration","mode":"heldout-model-output-calibration","cases":total,"correct":correct,"calibrated_accuracy":acc,"predicted_counts":dict(counts),"parse_mode_counts":dict(modes),"results":rows,"runtime_authority_granted":False,"provider_dispatch_enabled":False}
    out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("ZANT_LLM_V0_8R_CALIBRATION_ANALYZED=True"); print(f"CASES={total}"); print(f"CALIBRATED_ACCURACY={acc}"); print(f"REPORT={out}"); print("RUNTIME_AUTHORITY_GRANTED=False"); print("PROVIDER_DISPATCH_ENABLED=False")
if __name__=="__main__": main()
