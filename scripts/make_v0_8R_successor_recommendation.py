import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
report=json.loads((ROOT/"reports/v0_8R/zant_llm_v0_8R_calibrated_model_probe_report.json").read_text(encoding="utf-8"))
json_rate=report.get("parse_mode_counts",{}).get("json",0)/report["cases"]
acc=report["calibrated_accuracy"]
successor="v0.9-inference-contract-stabilization" if acc>=0.95 and json_rate<0.5 else "v0.9-small-scale-output-format-sft"
reason="Calibrated parser recovers decisions, but raw JSON rate is low; stabilize inference contract before more SFT." if successor.endswith("stabilization") else "Calibrated accuracy below threshold; train output format SFT."
out={"branch":"v0.8R-heldout-model-output-calibration","calibrated_accuracy":acc,"json_rate":json_rate,"recommended_successor":successor,"reason":reason,"runtime_authority_granted":False,"provider_dispatch_enabled":False}
p=ROOT/"reports/v0_8R/zant_llm_v0_8R_successor_recommendation.json"; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("ZANT_LLM_V0_8R_SUCCESSOR_RECOMMENDATION_CREATED=True"); print(f"SUCCESSOR={successor}"); print(f"REPORT={p}")
