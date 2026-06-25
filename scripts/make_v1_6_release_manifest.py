from pathlib import Path
import json, hashlib

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'release_manifests' / 'zant_llm_v1_6_release_manifest.json'
OUT.parent.mkdir(parents=True, exist_ok=True)

EXCLUDE = {
    'release_manifests/zant_llm_v1_6_release_manifest.json',
    'SHA256SUMS.txt',
}

files = []
for path in sorted(ROOT.rglob('*')):
    if not path.is_file():
        continue
    if '.git' in path.parts or '__pycache__' in path.parts or path.suffix == '.pyc':
        continue
    rel = path.relative_to(ROOT).as_posix()
    if rel in EXCLUDE:
        continue
    h = hashlib.sha256(path.read_bytes()).hexdigest()
    files.append({'path': rel, 'sha256': h, 'bytes': path.stat().st_size})

obj = {
    'version': 'v1.6',
    'branch': 'v1.6-runtime-observability-and-operator-dashboard',
    'created_at': '2026-06-25',
    'artifact_count': len(files),
    'files': files,
    'runtime_authority_granted': False,
    'provider_dispatch_enabled': False,
    'successor': 'v1.6R-runtime-observability-audit-and-dashboard-hardening',
    'note': 'release manifest excludes itself and SHA256SUMS.txt to avoid self-referential hash drift',
}
OUT.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding='utf-8')
print('ZANT_LLM_V1_6_RELEASE_MANIFEST_CREATED=True')
print(f'RELEASE_MANIFEST={OUT}')
