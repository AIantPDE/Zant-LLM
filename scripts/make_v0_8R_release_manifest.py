import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
files=[]
for p in sorted(ROOT.rglob("*")):
    if p.is_file() and ".git" not in p.parts and "__pycache__" not in p.parts and p.suffix!=".pyc":
        files.append({"path":p.relative_to(ROOT).as_posix(),"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"bytes":p.stat().st_size})
out={"branch":"v0.8R-heldout-model-output-calibration","file_count":len(files),"files":files,"runtime_authority_granted":False,"provider_dispatch_enabled":False}
op=ROOT/"release_manifests/zant_llm_v0_8R_release_manifest.json"; op.parent.mkdir(parents=True,exist_ok=True); op.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("ZANT_LLM_V0_8R_RELEASE_MANIFEST_CREATED=True"); print(f"RELEASE_MANIFEST={op}")
