from __future__ import annotations
import json
from pathlib import Path
from typing import Any
from .formatting import build_prompt, build_completion
REQUIRED={"case_id","gate_name","gate_result","bundle","readiness_vector","gate_report","target_output"}
def load_jsonl(path: str | Path) -> list[dict[str, Any]]:
    rows=[]
    with Path(path).open("r", encoding="utf-8") as f:
        for line in f:
            line=line.strip()
            if line: rows.append(json.loads(line))
    return rows
def validate_case(row: dict[str, Any]) -> None:
    missing=REQUIRED-set(row)
    if missing: raise ValueError(f"missing fields: {sorted(missing)}")
    if row["gate_result"] not in {"READY","BLOCKED","CLOSEOUT","FAILCLOSED"}: raise ValueError("bad gate result")
def to_sft(row: dict[str, Any]) -> dict[str, str]:
    validate_case(row)
    return {"id":row["case_id"],"prompt":build_prompt(row),"completion":build_completion(row),"text":build_prompt(row)+build_completion(row)}
