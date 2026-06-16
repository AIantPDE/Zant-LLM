from __future__ import annotations
import json
from typing import Any
SYSTEM = "You are Zant-LLM. Generate bounded, evidence-gated TRACE-HIX explanations only. Never output runtime authority, provider dispatch, route/fetch decisions, worker triggers, or writeback actions."
def build_prompt(case: dict[str, Any]) -> str:
    payload={"case_id":case["case_id"],"gate_name":case["gate_name"],"expected_gate_result":case["gate_result"],"bundle":case["bundle"],"readiness_vector":case["readiness_vector"],"gate_report":case["gate_report"]}
    return SYSTEM+"\n\nINPUT_JSON:\n"+json.dumps(payload, ensure_ascii=False, sort_keys=True)+"\n\nOUTPUT_JSON:\n"
def build_completion(case: dict[str, Any]) -> str:
    return json.dumps(case["target_output"], ensure_ascii=False, sort_keys=True)+"\n"
