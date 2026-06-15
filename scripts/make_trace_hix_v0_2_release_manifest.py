from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "release_manifests/trace_hix_v0_2_release_manifest.json"

TRACKED_PREFIXES = ["schemas", "registries", "src", "scripts", "tests", "data", "data_manifests", "reports", "docs"]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def main() -> int:
    files = []
    for prefix in TRACKED_PREFIXES:
        base = ROOT / prefix
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            if path.is_file() and not path.name.endswith(".pyc"):
                rel = path.relative_to(ROOT).as_posix()
                files.append({"path": rel, "sha256": sha256(path), "size_bytes": path.stat().st_size})
    manifest = {
        "manifest_version":"trace_hix_v0_2_release_manifest",
        "branch":"v0.2-trace-hix-contracts-and-validators",
        "base_branch":"v0.1-explanation-preview-baseline",
        "repository":"https://github.com/AIantPDE/Zant-LLM.git",
        "purpose":"TRACE-HIX contracts, registries, validators, gold/negative seeds, and validation reports.",
        "runtime_authority_granted":False,
        "provider_dispatch_enabled":False,
        "file_count":len(files),
        "files":files,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print("TRACE_HIX_V0_2_RELEASE_MANIFEST_CREATED=True")
    print(f"RELEASE_MANIFEST={OUT}")
    print("RUNTIME_AUTHORITY_GRANTED=False")
    print("PROVIDER_DISPATCH_ENABLED=False")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
