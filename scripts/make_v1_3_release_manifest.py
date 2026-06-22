from pathlib import Path
import json, hashlib
ROOT = Path(__file__).resolve().parents[1]

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()

def main():
    files=[]
    for p in sorted(ROOT.rglob('*')):
        if p.is_file() and '.git' not in p.parts and '__pycache__' not in p.parts and p.suffix != '.pyc':
            rel=p.relative_to(ROOT).as_posix()
            files.append({'path':rel,'sha256':sha(p),'bytes':p.stat().st_size})
    manifest={
        'manifest_version':'zant_llm_v1_3_release_manifest_v0',
        'branch':'v1.3-release-candidate-packaging',
        'base_branch':'v1.2-runtime-deployment-readiness',
        'file_count':len(files),
        'files':files,
        'runtime_authority_granted':False,
        'provider_dispatch_enabled':False,
    }
    p=ROOT/'release_manifests/zant_llm_v1_3_release_manifest.json'
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('ZANT_LLM_V1_3_RELEASE_MANIFEST_CREATED=True')
    print('RELEASE_MANIFEST='+str(p))
    return 0
if __name__=='__main__':
    raise SystemExit(main())
