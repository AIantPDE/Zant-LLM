import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()
def main():
    files=[]
    for rel in ['data/trace_hix_v0_4/sft_train_180.jsonl','data/trace_hix_v0_4/sft_eval_45.jsonl','reports/v0_4/zant_llm_v0_4_gate_aware_eval_report.json']:
        p=ROOT/rel
        if p.exists(): files.append({'path':rel,'sha256':sha(p),'size_bytes':p.stat().st_size})
    outdir=ROOT/'outputs/v0_4/gemma4_lora_adapter'
    if outdir.exists():
        for p in outdir.rglob('*'):
            if p.is_file() and p.name!='.gitkeep': files.append({'path':str(p.relative_to(ROOT)).replace('\\','/'),'sha256':sha(p),'size_bytes':p.stat().st_size})
    manifest={'release_manifest_version':'zant_llm_v0_4_release_manifest_v0','branch':'v0.4-evidence-gated-explanation-admissibility','runtime_authority_granted':False,'provider_dispatch_enabled':False,'files':files}
    out=ROOT/'release_manifests/zant_llm_v0_4_release_manifest.json'; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('ZANT_LLM_V0_4_RELEASE_MANIFEST_CREATED=True'); print(f'RELEASE_MANIFEST={out}'); return 0
if __name__=='__main__': raise SystemExit(main())

