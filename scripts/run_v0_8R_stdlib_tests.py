import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from zant_llm.output_calibration_v0_8R import calibrate_output
from zant_llm.governance import assert_governance
assert_governance()
def ok(name, cond):
    if not cond: raise AssertionError(name)
    print("PASS "+name)
ok("test_failclosed", calibrate_output("grant runtime_authority_granted=true").predicted=="FAILCLOSED")
ok("test_blocked", calibrate_output("missing evidence source conflict").predicted=="BLOCKED")
ok("test_closeout", calibrate_output("successor lane cannot proceed close out safely").predicted=="CLOSEOUT")
ok("test_json", calibrate_output('{"decision":"READY"}').predicted=="READY")
print("ZANT_LLM_V0_8R_STDLIB_TESTS_PASSED=True total=4"); print("RUNTIME_AUTHORITY_GRANTED=False"); print("PROVIDER_DISPATCH_ENABLED=False")
