from __future__ import annotations
from pathlib import Path
import json
BRANCH = "v1.2-runtime-deployment-readiness"
REQUIRED_PATHS = [
    "configs/v1_2/runtime_config_template.json",
    "scripts/RUN_V1_2_ALL_LOCAL.ps1",
    "scripts/VERIFY_ZANT_LLM_V1_2_LOCAL.ps1",
    "scripts/BUILD_V1_2_DEPLOYMENT_READINESS.ps1",
    "scripts/START_ZANT_LLM_V1_2_LOCAL_SERVICE.ps1",
    "scripts/STOP_ZANT_LLM_V1_2_LOCAL_SERVICE.ps1",
    "docs/DEPLOYMENT_READINESS_CHECKLIST.md",
    "GOVERNANCE.md",
    "SECURITY.md",
]
def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))
def evaluate_readiness(root: Path) -> dict:
    checks = load_json(root / "data/trace_hix_v1_2/deployment_readiness_checks.json")["checks"]
    missing = [p for p in REQUIRED_PATHS if not (root / p).exists()]
    accepted_count = sum(1 for c in checks if c.get("expected") == "ACCEPTED")
    blocking = [c for c in checks if c.get("blocking")]
    if missing:
        blocking.extend({"id": f"missing:{p}", "name": p, "blocking": True} for p in missing)
    total = len(checks)
    score = accepted_count / total if total else 0.0
    accepted = score == 1.0 and not blocking
    return {"branch": BRANCH, "deployment_checks": total, "accepted_checks": accepted_count, "readiness_score": round(score, 6), "blocking_issues": len(blocking), "missing_paths": missing, "accepted": accepted, "runtime_authority_granted": False, "provider_dispatch_enabled": False}
def build_artifact_inventory(root: Path) -> dict:
    artifacts = []
    for rel in ["configs/v1_2/runtime_config_template.json", "docs/V1_2_RUNTIME_DEPLOYMENT_READINESS.md", "reports/v1_2/zant_llm_v1_2_deployment_readiness_report.json", "reports/v1_2/zant_llm_v1_2_successor_recommendation.json", "release_manifests/zant_llm_v1_2_release_manifest.json"]:
        p = root / rel
        artifacts.append({"path": rel, "exists": p.exists(), "bytes": p.stat().st_size if p.exists() else 0})
    return {"branch": BRANCH, "artifact_count": len(artifacts), "artifacts": artifacts, "runtime_authority_granted": False, "provider_dispatch_enabled": False}
