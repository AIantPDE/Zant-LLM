from __future__ import annotations
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]

def load_jsonl(path: str | Path) -> list[dict[str, Any]]:
    p = Path(path)
    out = []
    with p.open('r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out

def load_heldout_eval() -> list[dict[str, Any]]:
    return load_jsonl(ROOT / 'data/trace_hix_v0_8/heldout_eval_180.jsonl')
