from __future__ import annotations
import hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def sha(p):
    h=hashlib.sha256();
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024), b''): h.update(b)
    return h.hexdigest()

def main():
    files=[]
    for rel in ['data/trace_hix_v0_6/realworld_eval_300.jsonl','reports/v0_6/zant_llm_v0_6_realworld_eval_report.json','README.md','VERSION']:
        p=ROOT/rel
        if p.exists(): files.append({'path':rel,'sha256':sha(p),'bytes':p.stat().st_size})
    manifest={
        'manifest_version':'zant_llm_v0_6_release_manifest_v0',
        'branch':'v0.6-realworld-adversarial-eval',
        'files':files,
        'runtime_authority_granted':False,
        'provider_dispatch_enabled':False,
    }
    out=ROOT/'release_manifests/zant_llm_v0_6_release_manifest.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('ZANT_LLM_V0_6_RELEASE_MANIFEST_CREATED=True')
    print(f'RELEASE_MANIFEST={out}')
    return 0
if __name__=='__main__': raise SystemExit(main())
