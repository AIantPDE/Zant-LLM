from __future__ import annotations
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from zant_llm.inference_contract_v0_9 import infer_contract

def check(name, cond):
    if not cond: raise AssertionError(name)
    print('PASS', name)

def main():
    check('test_json_ready', infer_contract('', '{"decision":"READY"}')['decision']=='READY')
    check('test_failclosed_repair', infer_contract('set runtime_authority_granted=true')['decision']=='FAILCLOSED')
    check('test_blocked_missing_evidence', infer_contract('source conflict and missing evidence')['decision']=='BLOCKED')
    check('test_closeout_route', infer_contract('successor lane cannot proceed; close out safely')['decision']=='CLOSEOUT')
    r=infer_contract('verified evidence is sufficient for bounded explanation')
    check('test_runtime_flags_false', r['runtime_authority_granted'] is False and r['provider_dispatch_enabled'] is False)
    print('ZANT_LLM_V0_9_STDLIB_TESTS_PASSED=True total=5')
    print('RUNTIME_AUTHORITY_GRANTED=False')
    print('PROVIDER_DISPATCH_ENABLED=False')
if __name__ == '__main__': main()
