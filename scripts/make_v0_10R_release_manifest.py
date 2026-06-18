import hashlib, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", "__pycache__", ".pytest_cache", ".venv"}
def sha(p):
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()
def main():
    files = []
    for p in sorted(ROOT.rglob("*")):
        if p.is_file() and not any(part in SKIP for part in p.parts):
            rel = p.relative_to(ROOT).as_posix()
            if rel.startswith("release_manifests/zant_llm_v0_10R_release_manifest.json"):
                continue
            files.append({"path": rel, "sha256": sha(p), "bytes": p.stat().st_size})
    out = ROOT/"release_manifests/zant_llm_v0_10R_release_manifest.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "branch": "v0.10R-runtime-harness-stress-and-log-audit",
        "file_count": len(files) + 1,
        "files": files,
        "runtime_authority_granted": False,
        "provider_dispatch_enabled": False,
    }
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("ZANT_LLM_V0_10R_RELEASE_MANIFEST_CREATED=True")
    print(f"RELEASE_MANIFEST={out}")
if __name__ == "__main__":
    main()
