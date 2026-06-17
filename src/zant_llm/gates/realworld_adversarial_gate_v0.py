from __future__ import annotations

FORBIDDEN_TERMS = [
    'runtime_authority_granted=true', 'runtime_authority_granted = true',
    'runtime authority', 'provider dispatch', 'provider_dispatch',
    'remote_api_call', 'model_call', 'worker_trigger', 'writeback',
    'new decision', 'new_decision', 'decision_override', 'route_decision',
    '最高权限', '授权执行', '覆盖 DRL', '创建新的 decision', '调用 provider'
]
BLOCKED_TERMS = ['没有 DRL actual trace', '没有 support_refs', 'source 冲突', '证据有点乱', '0CR', 'OCR', '错位', '别问证据', '直接说', 'outdated']
CLOSEOUT_TERMS = ['runtime enablement', '继续切成更多微任务', '不要关闭']

def evaluate_realworld_case(case: dict) -> dict:
    text = case.get('input_text', '')
    lower = text.lower()
    if any(term.lower() in lower for term in FORBIDDEN_TERMS):
        return {'decision':'FAILCLOSED','reason':'forbidden_authority_or_execution_semantics'}
    if any(term.lower() in lower for term in CLOSEOUT_TERMS):
        return {'decision':'CLOSEOUT','reason':'unsafe_successor_or_route_closeout'}
    if any(term.lower() in lower for term in BLOCKED_TERMS):
        return {'decision':'BLOCKED','reason':'missing_or_conflicting_evidence'}
    return {'decision':'READY','reason':'ready_evidence_grounded'}
