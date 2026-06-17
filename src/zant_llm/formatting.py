from __future__ import annotations
import json

def to_sft_text(prompt: str, completion: dict) -> str:
    return prompt.rstrip() + '\n\n### Response\n' + json.dumps(completion, ensure_ascii=False, sort_keys=True)
