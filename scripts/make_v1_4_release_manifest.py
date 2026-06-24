from pathlib import Path
import json, hashlib
ROOT=Path(__file__).resolve().parents[1]
files=[]
for p in sorted(ROOT.rglob('*')):
    if p.is_file() and '.git' not in p.parts and '__pycache__' not in p.parts and p.suffix!='.pyc':
        files.append({'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
man={'manifest_version':'zant_llm_v1_4_release_manifest_v0','branch':'v1.4-final-release-manifest-and-tagging','base_branch':'v1.3R-release-candidate-signoff-and-smoke','recommended_tag':'v1.4.0','file_count':len(files),'files':files,'runtime_authority_granted':False,'provider_dispatch_enabled':False}
out=ROOT/'release_manifests'; out.mkdir(parents=True,exist_ok=True); path=out/'zant_llm_v1_4_release_manifest.json'; path.write_text(json.dumps(man,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('ZANT_LLM_V1_4_RELEASE_MANIFEST_CREATED=True')
print('RELEASE_MANIFEST='+str(path))
