import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from zant_llm.governance import PROVIDER_DISPATCH_ENABLED, RUNTIME_AUTHORITY_GRANTED
from zant_llm.orsc_v6_gate import BLOCKED, CLOSEOUT, FAIL_CLOSED, READY, evaluate_gate, hydrate_successor_inputs, resolve_successor, seal_receipt, verify_receipt_hash
from zant_llm.gate_aware_observability_v1_6r import PROPOSED_SUCCESSOR, FALLBACK_SUCCESSOR, build_gate_report, build_successor_report

def run_test(name, fn): fn(); print(f"PASS {name}")
def test_flags_false(): assert RUNTIME_AUTHORITY_GRANTED is False and PROVIDER_DISPATCH_ENABLED is False
def test_ready_gate(): assert evaluate_gate({"readiness_vector":{"a":True,"runtime_authority_unchanged_false":True,"provider_dispatch_unchanged_false":True}})["gate_result"] == READY
def test_blocked_gate(): assert evaluate_gate({"readiness_vector":{"a":False,"runtime_authority_unchanged_false":True,"provider_dispatch_unchanged_false":True},"blocking_reasons":["a_false"]})["gate_result"] == BLOCKED
def test_closeout_gate(): assert evaluate_gate({"expected_gate_result":CLOSEOUT,"readiness_vector":{"route_has_safe_action_path":False,"runtime_authority_unchanged_false":True,"provider_dispatch_unchanged_false":True},"blocking_reasons":["route_closed_no_safe_action_path"]})["gate_result"] == CLOSEOUT
def test_forbidden_payload_fail_closed(): assert evaluate_gate({"payload":{"worker_trigger":False},"readiness_vector":{"runtime_authority_unchanged_false":True,"provider_dispatch_unchanged_false":True}})["gate_result"] == FAIL_CLOSED
def test_unknown_fail_closed(): assert evaluate_gate({"readiness_vector":{"a":"Unknown","runtime_authority_unchanged_false":True,"provider_dispatch_unchanged_false":True}})["gate_result"] == FAIL_CLOSED
def test_hydration_concrete(): assert hydrate_successor_inputs({"hydrated_inputs":{"a":True,"b":False}}) == {"a":True,"b":False}
def test_resolver(): assert resolve_successor(PROPOSED_SUCCESSOR, {"a":True,"b":True}, FALLBACK_SUCCESSOR)["actual_successor"] == PROPOSED_SUCCESSOR
def test_receipt_seal():
    receipt = seal_receipt({"a":1,"b":{"c":2}}); assert "hash" in receipt and verify_receipt_hash(receipt)
def test_gate_report_counts():
    report = build_gate_report(ROOT); assert report["ok"] is True; assert report["counts"][READY] == 12; assert report["counts"][BLOCKED] == 12; assert report["counts"][CLOSEOUT] == 12; assert report["counts"][FAIL_CLOSED] == 24
def test_successor_report(): assert build_successor_report(ROOT)["actual_successor"] == PROPOSED_SUCCESSOR

def main():
    tests = [("test_flags_false", test_flags_false),("test_ready_gate", test_ready_gate),("test_blocked_gate", test_blocked_gate),("test_closeout_gate", test_closeout_gate),("test_forbidden_payload_fail_closed", test_forbidden_payload_fail_closed),("test_unknown_fail_closed", test_unknown_fail_closed),("test_hydration_concrete", test_hydration_concrete),("test_resolver", test_resolver),("test_receipt_seal", test_receipt_seal),("test_gate_report_counts", test_gate_report_counts),("test_successor_report", test_successor_report)]
    for name, fn in tests: run_test(name, fn)
    print(f"ZANT_LLM_V1_6R_STDLIB_TESTS_PASSED=True total={len(tests)}")
    print("RUNTIME_AUTHORITY_GRANTED=False")
    print("PROVIDER_DISPATCH_ENABLED=False")
if __name__ == "__main__": main()
