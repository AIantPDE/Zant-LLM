from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def load_jsonl(path: str | Path):
    p = Path(path)
    return [json.loads(line) for line in p.read_text(encoding='utf-8').splitlines() if line.strip()]
