from pathlib import Path
import json, hashlib
ROOT=Path(__file__).resolve().parents[1]
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1048576), b''):
            h.update(chunk)
    return h.hexdigest()
def main():
    files=[]
    for rel in [
        'README.md','DELIVERY_MANIFEST_V1_3R.json','reports/v1_3R/zant_llm_v1_3R_rc_signoff_report.json',
        'reports/v1_3R/zant_llm_v1_3R_smoke_report.json','reports/v1_3R/zant_llm_v1_3R_successor_recommendation.json',
        'src/zant_llm/rc_signoff_v1_3r.py'
    ]:
        p=ROOT/rel
        files.append({'path':rel,'exists':p.exists(),'sha256':sha(p) if p.exists() else None})
    manifest={
        'manifest_version':'zant_llm_v1_3R_release_manifest_v0',
        'branch':'v1.3R-release-candidate-signoff-and-smoke',
        'base_branch':'v1.3-release-candidate-packaging',
        'successor':'v1.4-final-release-manifest-and-tagging',
        'files':files,
        'runtime_authority_granted':False,
        'provider_dispatch_enabled':False,
    }
    path=ROOT/'release_manifests/zant_llm_v1_3R_release_manifest.json'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('ZANT_LLM_V1_3R_RELEASE_MANIFEST_CREATED=True')
    print('RELEASE_MANIFEST='+str(path))
    return 0
if __name__=='__main__':
    raise SystemExit(main())
