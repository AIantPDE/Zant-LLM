import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "v0_1"
REL = ROOT / "release_manifests"
REL.mkdir(parents=True, exist_ok=True)

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> int:
    required = [OUT / "model_artifact.json", OUT / "train_report.json", OUT / "eval_report.json", OUT / "predictions.jsonl"]
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        raise FileNotFoundError("Missing files for release manifest: " + ", ".join(missing))
    manifest = {"release": "zant-llm-v0.1-explanation-preview-baseline", "branch": "v0.1-explanation-preview-baseline", "artifact_type": "local_text_baseline", "files": [{"path": str(p.relative_to(ROOT)).replace("\\", "/"), "sha256": sha256_file(p)} for p in required], "runtime_authority_granted": False, "provider_dispatch_enabled": False, "provider_registry_changed": False}
    path = REL / "zant_llm_v0_1_release_manifest.json"
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print("ZANT_LLM_V0_1_RELEASE_MANIFEST_CREATED=True")
    print(f"RELEASE_MANIFEST={path}")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
