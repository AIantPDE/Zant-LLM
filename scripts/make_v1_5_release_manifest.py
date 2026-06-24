import json, hashlib
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
files=[]
for p in sorted(ROOT.rglob('*')):
    if p.is_file() and '.git' not in p.parts:
        rel = p.relative_to(ROOT).as_posix()
        if rel == 'release_manifests/zant_llm_v1_5_release_manifest.json':
            continue
        files.append({'path': rel, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'bytes': p.stat().st_size})
manifest = {
  'manifest_version': 'zant_llm_v1_5_release_manifest_v0',
  'branch': 'v1.5-post-release-monitoring-and-maintenance',
  'base_branch': 'v1.4R-final-release-smoke-and-archive',
  'release_tag_under_watch': 'v1.4.0',
  'file_count': len(files),
  'files': files,
  'runtime_authority_granted': False,
  'provider_dispatch_enabled': False,
}
out = ROOT/'release_manifests/zant_llm_v1_5_release_manifest.json'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
print('ZANT_LLM_V1_5_RELEASE_MANIFEST_CREATED=True')
print('RELEASE_MANIFEST=' + str(out))
