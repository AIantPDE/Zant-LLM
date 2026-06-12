from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from zant_llm.governance import BOUNDARY_FLAGS, assert_runtime_boundaries  # noqa: E402
from zant_llm.schema import validate_record  # noqa: E402

REQUIRED_FILES = [
    "README.md",
    "GOVERNANCE.md",
    "TRAINING_LANE_REGISTRY.md",
    "MODEL_CARD_TEMPLATE.md",
    "RELEASE_POLICY.md",
    "SECURITY.md",
    "VERSION",
    "configs/zant_llm_v0_1_baseline_config.json",
    "data/seed/zant_llm_v0_1_seed_30.jsonl",
    "data_manifests/zant_llm_v0_1_seed_manifest.json",
    "src/zant_llm/governance.py",
    "src/zant_llm/schema.py",
    "src/zant_llm/baseline.py",
]

FORBIDDEN_WEIGHT_SUFFIXES = {
    ".safetensors",
    ".gguf",
    ".bin",
    ".pt",
    ".pth",
    ".ckpt",
    ".onnx",
}


def main() -> int:
    missing = [rel for rel in REQUIRED_FILES if not (ROOT / rel).exists()]
    if missing:
        raise SystemExit(f"ZANT_LLM_V0_1_REQUIRED_FILES_MISSING: {missing}")

    assert_runtime_boundaries()
    if BOUNDARY_FLAGS["runtime_authority_granted"] is not False:
        raise SystemExit("ZANT_LLM_V0_1_RUNTIME_AUTHORITY_MUST_BE_FALSE")

    weight_files = [
        str(path.relative_to(ROOT))
        for path in ROOT.rglob("*")
        if path.is_file() and path.suffix.lower() in FORBIDDEN_WEIGHT_SUFFIXES
    ]
    if weight_files:
        raise SystemExit(f"ZANT_LLM_V0_1_FORBIDDEN_WEIGHT_FILES_PRESENT: {weight_files}")

    seed_path = ROOT / "data/seed/zant_llm_v0_1_seed_30.jsonl"
    records = []
    for line_no, line in enumerate(seed_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
            validate_record(record)
            records.append(record)
        except Exception as exc:  # noqa: BLE001
            raise SystemExit(f"ZANT_LLM_V0_1_SEED_INVALID line={line_no} error={exc}") from exc

    if len(records) != 30:
        raise SystemExit(f"ZANT_LLM_V0_1_SEED_COUNT_INVALID expected=30 observed={len(records)}")

    print("ZANT_LLM_V0_1_PACK_VALID=True")
    print(f"ZANT_LLM_V0_1_SEED_COUNT={len(records)}")
    print("RUNTIME_AUTHORITY_GRANTED=False")
    print("PROVIDER_DISPATCH_ENABLED=False")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
