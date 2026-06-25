from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()

    files = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if rel.startswith(".git/") or "__pycache__" in rel:
            continue
        files.append({
            "path": rel,
            "sha256": sha256_file(path),
            "bytes": path.stat().st_size,
        })

    audit_report_path = root / "reports/v1_5R/zant_llm_v1_5R_audit_report.json"
    audit_report = json.loads(audit_report_path.read_text(encoding="utf-8")) if audit_report_path.exists() else {}

    manifest = {
        "version": "v1.5R",
        "branch": "v1.5R-post-release-monitoring-audit-and-hotfix-readiness",
        "baseline": "v1.5-post-release-monitoring-and-maintenance",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "recommended_successor": "v1.6-runtime-observability-and-operator-dashboard",
        "audit_report": audit_report,
        "files": files,
        "runtime_authority_granted": False,
        "provider_dispatch_enabled": False,
    }

    out = root / "release_manifests/zant_llm_v1_5R_release_manifest.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("ZANT_LLM_V1_5R_RELEASE_MANIFEST_CREATED=True")
    print(f"RELEASE_MANIFEST={out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
