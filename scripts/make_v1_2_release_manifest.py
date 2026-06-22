from pathlib import Path
import hashlib, json
ROOT=Path(__file__).resolve().parents[1]
def sha256(p):
    h=hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()
def main():
    files=[]
    for p in sorted(ROOT.rglob('*')):
        if p.is_file() and '.git' not in p.parts and '__pycache__' not in p.parts and p.suffix!='.pyc':
            rel=p.relative_to(ROOT).as_posix()
            files.append({'path':rel,'sha256':sha256(p),'bytes':p.stat().st_size})
    obj={'branch':'v1.2-runtime-deployment-readiness','file_count':len(files),'files':files,'runtime_authority_granted':False,'provider_dispatch_enabled':False}
    out=ROOT/'release_manifests/zant_llm_v1_2_release_manifest.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('ZANT_LLM_V1_2_RELEASE_MANIFEST_CREATED=True')
    print('RELEASE_MANIFEST='+str(out))
    return 0
if __name__=='__main__': raise SystemExit(main())
