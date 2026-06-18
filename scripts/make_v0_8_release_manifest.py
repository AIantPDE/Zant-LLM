from __future__ import annotations
import json, hashlib
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def sha(p: Path) -> str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024), b''):
            h.update(b)
    return h.hexdigest()

def main() -> int:
    files=[]
    for p in ROOT.rglob('*'):
        if p.is_file() and '.git' not in p.parts and '__pycache__' not in p.parts and p.suffix != '.pyc':
            files.append({'path':str(p.relative_to(ROOT)).replace('\\','/'), 'sha256':sha(p), 'bytes':p.stat().st_size})
    manifest={'branch':'v0.8-heldout-model-eval','file_count':len(files),'files':files,'runtime_authority_granted':False,'provider_dispatch_enabled':False}
    out=ROOT/'release_manifests/zant_llm_v0_8_release_manifest.json'; out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('ZANT_LLM_V0_8_RELEASE_MANIFEST_CREATED=True')
    print(f'RELEASE_MANIFEST={out}')
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
