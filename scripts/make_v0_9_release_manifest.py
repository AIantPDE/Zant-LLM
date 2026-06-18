from __future__ import annotations
import hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def sha(p):
    h=hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()

def main():
    files=[]
    for p in sorted(ROOT.rglob('*')):
        if p.is_file() and '.git' not in p.parts and '__pycache__' not in p.parts and p.suffix!='.pyc':
            files.append({'path':str(p.relative_to(ROOT)).replace('\\','/'),'sha256':sha(p),'bytes':p.stat().st_size})
    out=ROOT/'release_manifests/zant_llm_v0_9_release_manifest.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    obj={'branch':'v0.9-inference-contract-stabilization','file_count':len(files),'files':files,'runtime_authority_granted':False,'provider_dispatch_enabled':False}
    out.write_text(json.dumps(obj,ensure_ascii=False,indent=2), encoding='utf-8')
    print('ZANT_LLM_V0_9_RELEASE_MANIFEST_CREATED=True')
    print(f'RELEASE_MANIFEST={out}')
if __name__=='__main__': main()
