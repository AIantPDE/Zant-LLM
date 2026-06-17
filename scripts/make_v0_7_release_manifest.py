from pathlib import Path
import json, hashlib, time
ROOT=Path(__file__).resolve().parents[1]
def sha(p):
    h=hashlib.sha256();
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576), b''): h.update(b)
    return h.hexdigest()
files=[]
for p in sorted(ROOT.rglob('*')):
    if p.is_file() and '.git' not in p.parts and '__pycache__' not in p.parts:
        files.append({'path':str(p.relative_to(ROOT)).replace('\\','/'),'sha256':sha(p),'bytes':p.stat().st_size})
manifest={'manifest_version':'zant_llm_v0_7_release_manifest_v1','branch':'v0.7-calibration-informed-sft','created_at_unix':time.time(),'file_count':len(files),'files':files,'runtime_authority_granted':False,'provider_dispatch_enabled':False}
out=ROOT/'release_manifests/zant_llm_v0_7_release_manifest.json'; out.parent.mkdir(exist_ok=True); out.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('ZANT_LLM_V0_7_RELEASE_MANIFEST_CREATED=True')
print(f'RELEASE_MANIFEST={out}')
