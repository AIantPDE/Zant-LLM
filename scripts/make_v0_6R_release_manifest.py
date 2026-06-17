from pathlib import Path
import json, hashlib, time
ROOT=Path(__file__).resolve().parents[1]
def sha(p): h=hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()
def main():
    files=[]
    for p in sorted(ROOT.rglob('*')):
        if p.is_file() and '.git' not in p.parts and '__pycache__' not in p.parts and p.suffix != '.pyc':
            files.append({'path':str(p.relative_to(ROOT)).replace('\\','/'), 'sha256':sha(p), 'bytes':p.stat().st_size})
    manifest={'manifest_version':'zant_llm_v0_6R_release_manifest_v1','branch':'v0.6R-realworld-eval-calibration','created_at_unix':int(time.time()),'file_count':len(files),'files':files,'runtime_authority_granted':False,'provider_dispatch_enabled':False}
    out=ROOT/'release_manifests/zant_llm_v0_6R_release_manifest.json'; out.parent.mkdir(parents=True, exist_ok=True); out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('ZANT_LLM_V0_6R_RELEASE_MANIFEST_CREATED=True')
    print(f'RELEASE_MANIFEST={out}')
    return 0
if __name__=='__main__': raise SystemExit(main())
