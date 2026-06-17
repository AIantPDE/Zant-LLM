from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "trace_hix_v0_7"

def load_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

def train_cases():
    return load_jsonl(DATA_DIR / "calibration_train_360.jsonl")

def eval_cases():
    return load_jsonl(DATA_DIR / "calibration_eval_90.jsonl")
