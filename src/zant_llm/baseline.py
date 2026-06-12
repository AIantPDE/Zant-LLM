"""Template baseline for v0.1 explanation preview generation.

This is not a trained model. It is a deterministic baseline used to verify the
initial branch shape before real training code is added.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .governance import assert_runtime_boundaries
from .schema import validate_output_fields


def generate_template_explanation(record: Mapping[str, Any]) -> dict[str, str]:
    assert_runtime_boundaries()
    input_obj = record["input"]
    semantic_preview = input_obj["semantic_preview"]
    scenario = semantic_preview.get("scenario", "unknown")
    reason_codes = ", ".join(input_obj.get("reason_codes", [])) or "none"
    evidence_count = len(input_obj.get("evidence_references", []))

    output = {
        "explanation_summary": (
            f"这是一个 {scenario} 类型的解释预览样本；当前只能基于已给出的语义预览和证据引用进行说明。"
        ),
        "explanation_residual_hint": (
            f"残余提示：reason_codes={reason_codes}。如果证据不足，应保持保守解释。"
        ),
        "evidence_grounded_rationale": (
            f"当前输入包含 {evidence_count} 个 evidence_references；解释不得扩展到未提供的来源。"
        ),
        "uncertainty_aware_wording": "建议使用不确定性措辞，避免把预览解释包装成最终事实或操作建议。",
        "fail_closed_fallback": "如果字段冲突、证据不足或治理边界不清晰，应 fail-closed 并停止输出运行时动作。",
    }
    validate_output_fields(output)
    return output
