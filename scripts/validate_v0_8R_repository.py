from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
required=["data/trace_hix_v0_8R/calibration_probe_cases_12.jsonl","scripts/analyze_v0_8R_model_output_calibration.py","src/zant_llm/output_calibration_v0_8R.py"]
for rel in required:
    if not (ROOT/rel).exists(): raise SystemExit(f"missing {rel}")
rows=[json.loads(x) for x in (ROOT/"data/trace_hix_v0_8R/calibration_probe_cases_12.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
if len(rows)!=12: raise SystemExit(f"expected 12 rows, got {len(rows)}")
print("ZANT_LLM_V0_8R_REPOSITORY_VALID=True"); print("PROBE_SNAPSHOT_CASES=12"); print("RUNTIME_AUTHORITY_GRANTED=False"); print("PROVIDER_DISPATCH_ENABLED=False")
