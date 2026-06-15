from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"src"))
from zant_llm.v0_3_dataset import load_jsonl
from zant_llm.validators.reference_closure_validator_v0 import validate_reference_closure
from zant_llm.validators.claim_support_validator_v0 import validate_claim_support
from zant_llm.validators.forbidden_output_scanner_v0 import validate_forbidden_output
from zant_llm.validators.authority_leakage_scanner_v0 import validate_authority_leakage
from zant_llm.governance import assert_runtime_boundaries

def test_validators_pass_gold():
    case=load_jsonl(ROOT/"data/trace_hix_v0_3/trace_hix_v0_3_eval_cases_12.jsonl")[0]; exp=case["target_explanation"]
    assert validate_reference_closure(case["bundle"], exp)["passed"]
    assert validate_claim_support(case["bundle"], exp)["passed"]
    assert validate_forbidden_output(exp)["passed"]
    assert validate_authority_leakage(exp)["passed"]
def test_runtime_flags_false(): assert_runtime_boundaries()
