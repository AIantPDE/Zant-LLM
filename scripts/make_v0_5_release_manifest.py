import json, hashlib, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    files = []
    for p in sorted(ROOT.rglob('*')):
        if p.is_file() and '.git' not in p.parts and '__pycache__' not in p.parts and p.suffix != '.pyc':
            files.append({'path': p.relative_to(ROOT).as_posix(), 'sha256': sha(p), 'bytes': p.stat().st_size})
    out = ROOT / 'release_manifests/zant_llm_v0_5_release_manifest.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        'manifest_version': 'zant_llm_v0_5_release_manifest_v1',
        'branch': 'v0.5-adversarial-hard-cases-and-failclosed-eval',
        'file_count': len(files),
        'created_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'runtime_authority_granted': False,
        'provider_dispatch_enabled': False,
        'files': files,
    }, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('ZANT_LLM_V0_5_RELEASE_MANIFEST_CREATED=True')
    print(f'RELEASE_MANIFEST={out}')

if __name__ == '__main__':
    main()
