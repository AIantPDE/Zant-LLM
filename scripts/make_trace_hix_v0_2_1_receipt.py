from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> int:
    report_path = ROOT / "reports/v0_2_1/trace_hix_v0_2_1_gate_report.json"
    report = json.loads(report_path.read_text(encoding="utf-8")) if report_path.exists() else {}
    receipt = {
        "receipt_id": "trace_hix_v0_2_1_orsc_gate_alignment_receipt_v0",
        "lane": "v0.2.1-trace-hix-orsc-gate-alignment",
        "predecessor_ref": "v0.2-trace-hix-contracts-and-validators",
        "gate_result": "READY" if report.get("failed") == 0 else "BLOCKED",
        "successor_candidates": ["v0.3-gemma4-qlora-explanation-baseline", "v0.4-evidence-gated-explanation-admissibility"],
        "actual_successor": "v0.4-evidence-gated-explanation-admissibility" if report.get("failed") == 0 else None,
        "missing_evidence": [] if report.get("failed") == 0 else ["gate tests not passed"],
        "report_sha256": sha(report_path) if report_path.exists() else None,
        "runtime_authority_granted": False,
        "provider_dispatch_enabled": False,
    }
    canonical = json.dumps(receipt, sort_keys=True, ensure_ascii=False).encode("utf-8")
    receipt["receipt_hash"] = hashlib.sha256(canonical).hexdigest()
    out = ROOT / "release_manifests/trace_hix_v0_2_1_release_manifest.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print("TRACE_HIX_V0_2_1_RELEASE_MANIFEST_CREATED=True")
    print(f"RELEASE_MANIFEST={out}")
    print("RUNTIME_AUTHORITY_GRANTED=False")
    print("PROVIDER_DISPATCH_ENABLED=False")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
