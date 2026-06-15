from __future__ import annotations
import json

SYSTEM_PROMPT = """你是 Zant-LLM TRACE-HIX explanation generator。
你只能基于 DRL decision preview、DRL actual decision trace 和 bounded evidence projections 生成解释。
你不能生成 route_decision、fetch_decision、provider_dispatch、worker_trigger、writeback_execution、runtime_authority 或 new_decision。
输出必须是 TRACE_HIX_HUMAN_EXPLANATION_PREVIEW_V0 JSON。"""

def make_prompt(bundle: dict, human_query: str | None = None) -> str:
    query = human_query or bundle.get("interaction_context", {}).get("human_query", "请解释当前决策预览。")
    return (
        "<start_of_turn>system\n" + SYSTEM_PROMPT + "\n<end_of_turn>\n"
        "<start_of_turn>user\n"
        "human_query:\n" + query + "\n\n"
        "trace_hix_bundle_json:\n" + json.dumps(bundle, ensure_ascii=False, indent=2) + "\n"
        "<end_of_turn>\n"
        "<start_of_turn>model\n"
    )

def make_completion(target_explanation: dict) -> str:
    return json.dumps(target_explanation, ensure_ascii=False, indent=2) + "\n<end_of_turn>"

def make_sft_record(case: dict) -> dict:
    prompt = make_prompt(case["bundle"])
    completion = make_completion(case["target_explanation"])
    return {"case_id": case["case_id"], "prompt": prompt, "completion": completion, "text": prompt + completion}
