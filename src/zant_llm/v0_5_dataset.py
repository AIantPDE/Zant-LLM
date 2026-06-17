from __future__ import annotations
import json
from pathlib import Path
from typing import Any

def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    return [json.loads(x) for x in Path(path).read_text(encoding='utf-8').splitlines() if x.strip()]

def make_prompt(case: dict[str, Any]) -> str:
    return (
        'You are Zant-LLM v0.5. Generate only a gate-aware explanation artifact. '
        'Do not create decisions, routes, provider dispatch, runtime authority, fetch calls, worker triggers, or writeback execution.\n'
        f"CASE_ID={case['case_id']}\n"
        f"FAMILY={case['family']}\n"
        f"GATE={case['gate']}\n"
        'INPUT_JSON=' + json.dumps(case['input'], ensure_ascii=False, sort_keys=True)
    )

def make_sft_row(case: dict[str, Any]) -> dict[str, str]:
    prompt = make_prompt(case)
    comp = json.dumps(case['expected_completion'], ensure_ascii=False, sort_keys=True)
    return {
        'case_id': case['case_id'],
        'family': case['family'],
        'prompt': prompt,
        'completion': comp,
        'text': prompt.rstrip() + '\n\n### Response\n' + comp,
    }
