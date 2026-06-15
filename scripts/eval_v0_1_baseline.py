import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from zant_llm.baseline import read_jsonl, predict, write_json, write_jsonl
from zant_llm.governance import assert_no_forbidden_output


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
    out_dir = ROOT / config["output_dir"]
    model_path = out_dir / "model_artifact.json"
    eval_path = ROOT / config["eval_data"]
    if not model_path.exists():
        raise FileNotFoundError(f"Model artifact not found: {model_path}. Run train first.")
    model = json.loads(model_path.read_text(encoding="utf-8"))
    rows = read_jsonl(eval_path)
    preds = []
    correct = 0
    for row in rows:
        pred = predict(model, row)
        assert_no_forbidden_output(pred["prediction"])
        if pred["predicted_category"] == row.get("category"):
            correct += 1
        preds.append({"id": row.get("id"), "gold_category": row.get("category"), **pred})
    predictions_path = out_dir / "predictions.jsonl"
    write_jsonl(predictions_path, preds)
    report = {"ok": True, "version": "v0.1", "eval_count": len(rows), "category_accuracy": round(correct / max(1, len(rows)), 4), "model_sha256": sha256_file(model_path), "predictions_sha256": sha256_file(predictions_path), "runtime_authority_granted": False, "provider_dispatch_enabled": False}
    write_json(out_dir / "eval_report.json", report)
    print("ZANT_LLM_V0_1_EVALUATED=True")
    print(f"CATEGORY_ACCURACY={report['category_accuracy']}")
    print("RUNTIME_AUTHORITY_GRANTED=False")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
