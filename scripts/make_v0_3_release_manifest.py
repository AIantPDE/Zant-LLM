import json, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(path: Path):
    if not path.exists(): return None
    h=hashlib.sha256(); h.update(path.read_bytes()); return h.hexdigest()
def count(path: Path): return sum(1 for line in path.open("r", encoding="utf-8") if line.strip()) if path.exists() else 0
def main():
    train=ROOT/"data/trace_hix_v0_3/sft_train_60.jsonl"; ev=ROOT/"data/trace_hix_v0_3/sft_eval_12.jsonl"; report=ROOT/"reports/v0_3/zant_llm_v0_3_eval_report.json"
    m={"release_manifest_version":"zant_llm_v0_3_release_manifest_v0","branch":"v0.3-gemma4-qlora-explanation-baseline","base_branch":"v0.2-trace-hix-contracts-and-validators","train_sft_count":count(train),"train_sft_sha256":sha(train),"eval_sft_count":count(ev),"eval_sft_sha256":sha(ev),"eval_report_sha256":sha(report),"runtime_authority_granted":False,"provider_dispatch_enabled":False}
    out=ROOT/"release_manifests/zant_llm_v0_3_release_manifest.json"; out.parent.mkdir(parents=True, exist_ok=True); out.write_text(json.dumps(m, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print("ZANT_LLM_V0_3_RELEASE_MANIFEST_CREATED=True"); print(f"RELEASE_MANIFEST={out}"); return 0
if __name__ == "__main__": raise SystemExit(main())
