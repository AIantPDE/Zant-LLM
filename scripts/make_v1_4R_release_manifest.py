from pathlib import Path
import json, hashlib
ROOT = Path(__file__).resolve().parents[1]
out = ROOT / 'release_manifests/zant_llm_v1_4R_release_manifest.json'
out.parent.mkdir(parents=True, exist_ok=True)
files = []
for p in sorted(ROOT.rglob('*')):
    if p.is_file() and '.git' not in p.parts and '__pycache__' not in p.parts and p.suffix != '.pyc':
        rel = p.relative_to(ROOT).as_posix()
        if rel == 'release_manifests/zant_llm_v1_4R_release_manifest.json':
            continue
        files.append({'path': rel, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'bytes': p.stat().st_size})
obj = {
    'manifest_version': 'zant_llm_v1_4R_release_manifest_v0',
    'branch': 'v1.4R-final-release-smoke-and-archive',
    'base_branch': 'v1.4-final-release-manifest-and-tagging',
    'recommended_tag': 'v1.4.0',
    'file_count': len(files),
    'files': files,
    'runtime_authority_granted': False,
    'provider_dispatch_enabled': False,
}
out.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print('ZANT_LLM_V1_4R_RELEASE_MANIFEST_CREATED=True')
print('RELEASE_MANIFEST=' + str(out))
