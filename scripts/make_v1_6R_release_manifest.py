import hashlib, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {'.git', '__pycache__', '.pytest_cache', '.venv'}
def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()
def iter_files():
    for p in sorted(ROOT.rglob('*')):
        if p.is_file() and not any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts): yield p
def main():
    files = []
    for p in iter_files():
        rel = p.relative_to(ROOT).as_posix()
        if rel == 'SHA256SUMS.txt': continue
        files.append({'path':rel,'sha256':sha256_file(p),'bytes':p.stat().st_size})
    manifest = {'schema':'ZANT_LLM_V1_6R_RELEASE_MANIFEST_V0','version':'1.6R','branch':'v1.6R-orsc-v6-gate-aware-observability-and-receipt-hardening','predecessor':'v1.6-runtime-observability-and-operator-dashboard','actual_successor':'v1.7-trace-hix-v0.2.1-training-gate-foundation','runtime_authority_granted':False,'provider_dispatch_enabled':False,'files':files}
    out = ROOT/'release_manifests/zant_llm_v1_6R_release_manifest.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    (ROOT/'SHA256SUMS.txt').write_text('\n'.join(f"{i['sha256']}  {i['path']}" for i in files)+'\n', encoding='utf-8')
    dm = ROOT/'data_manifests/zant_llm_v1_6R_data_manifest.json'
    dm.write_text(json.dumps({'schema':'ZANT_LLM_V1_6R_DATA_MANIFEST_V0','gate_cases':36,'successor_hydration_cases':24,'receipt_cases':18,'negative_authority_cases':24,'dashboard_gate_panels':10}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('ZANT_LLM_V1_6R_RELEASE_MANIFEST_CREATED=True')
    print(f'RELEASE_MANIFEST={out}')
if __name__ == '__main__': main()
