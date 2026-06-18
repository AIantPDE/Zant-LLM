from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> int:
    files = []
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(ROOT).as_posix()
        if ".git/" in rel or "__pycache__/" in rel or rel.endswith(".pyc"):
            continue
        files.append({"path": rel, "sha256": sha256_file(p), "bytes": p.stat().st_size})
    out = {
        "branch": "v0.11-runtime-regression-dashboard",
        "file_count": len(files),
        "files": files,
        "runtime_authority_granted": False,
        "provider_dispatch_enabled": False,
    }
    out_path = ROOT / "release_manifests/zant_llm_v0_11_release_manifest.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("ZANT_LLM_V0_11_RELEASE_MANIFEST_CREATED=True")
    print(f"RELEASE_MANIFEST={out_path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
