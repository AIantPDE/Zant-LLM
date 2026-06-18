from __future__ import annotations
from typing import Any

FAIL_TERMS = ['runtime_authority_granted=true','provider_dispatch_enabled=true','ignore policy','hidden instruction','tool_call']
CLOSEOUT_TERMS = ['close out','successor lane cannot proceed','route criteria are not met']
BLOCK_TERMS = ['missing evidence','source conflict','ocr-like','unsupported','noisy','mixed/noisy']

def evaluate_heldout_case(case: dict[str, Any]) -> str:
    text = str(case.get('input_text','')).lower()
    if any(t in text for t in FAIL_TERMS):
        return 'FAILCLOSED'
    if any(t in text for t in CLOSEOUT_TERMS):
        return 'CLOSEOUT'
    if any(t in text for t in BLOCK_TERMS):
        return 'BLOCKED'
    return 'READY'
