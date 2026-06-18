from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
files=[]
for p in sorted(ROOT.rglob('*')):
    if not p.is_file(): continue
    rel=p.relative_to(ROOT).as_posix()
    if rel.startswith('.git/') or '__pycache__' in rel or rel.endswith('.pyc'): continue
    data=p.read_bytes()
    files.append({'path':rel,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
out=ROOT/'release_manifests/zant_llm_v0_10_release_manifest.json'; out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps({'branch':'v0.10-runtime-api-batch-harness','file_count':len(files),'files':files,'runtime_authority_granted':False,'provider_dispatch_enabled':False},ensure_ascii=False,indent=2),encoding='utf-8')
print('ZANT_LLM_V0_10_RELEASE_MANIFEST_CREATED=True')
print('RELEASE_MANIFEST='+str(out))
