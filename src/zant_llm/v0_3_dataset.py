from __future__ import annotations
import json
from pathlib import Path
from .formatting import make_sft_record

def load_jsonl(path: str | Path) -> list[dict]:
    rows = []
    with Path(path).open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows

def write_jsonl(path: str | Path, rows: list[dict]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

def build_sft_dataset(case_path: str | Path, output_path: str | Path) -> int:
    records = [make_sft_record(case) for case in load_jsonl(case_path)]
    write_jsonl(output_path, records)
    return len(records)
