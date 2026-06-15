import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from zant_llm.baseline import train_baseline, write_json


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/v0_1_train_config.json")
    args = parser.parse_args()
    config = json.loads((ROOT / args.config).read_text(encoding="utf-8"))
    train_path = ROOT / config["train_data"]
    out_dir = ROOT / config["output_dir"]
    out_dir.mkdir(parents=True, exist_ok=True)
    model = train_baseline(train_path)
    model_path = out_dir / "model_artifact.json"
    write_json(model_path, model)
    report = {"ok": True, "version": "v0.1", "model_path": str(model_path.relative_to(ROOT)), "train_data": config["train_data"], "train_sha256": sha256_file(train_path), "model_sha256": sha256_file(model_path), "example_count": model["example_count"], "category_counts": model["category_counts"], "runtime_authority_granted": False, "provider_dispatch_enabled": False}
    write_json(out_dir / "train_report.json", report)
    print("ZANT_LLM_V0_1_TRAINED=True")
    print(f"MODEL_PATH={model_path}")
    print(f"MODEL_SHA256={report['model_sha256']}")
    print("RUNTIME_AUTHORITY_GRANTED=False")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
