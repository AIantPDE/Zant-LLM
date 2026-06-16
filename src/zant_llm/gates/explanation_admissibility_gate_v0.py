from __future__ import annotations

from typing import Any

from .common import GateDecision, contains_forbidden_key, evaluate_readiness_vector


class ExplanationAdmissibilityGate:
    name = "ExplanationAdmissibilityGate"
    action_type = "explanation_output"

    def evaluate(self, payload: dict[str, Any]) -> GateDecision:
        readiness = dict(payload.get("readiness_vector", {}))

        runtime_authority_granted = payload.get("runtime_authority_granted")
        provider_dispatch_enabled = payload.get("provider_dispatch_enabled")

        readiness.setdefault("authority_boundary_declared", runtime_authority_granted is False)
        readiness.setdefault("provider_dispatch_disabled", provider_dispatch_enabled is False)

        # Gate 输入元数据可以声明 runtime_authority_granted=False / provider_dispatch_enabled=False。
        # 禁止字段扫描只应该扫描解释输出本体，不能把输入治理元数据当成模型输出。
        if runtime_authority_granted is not False:
            return GateDecision(
                self.name,
                self.action_type,
                "FAILCLOSED",
                readiness,
                blocking_residuals=["runtime_authority_granted"],
                reason="runtime authority must not be granted for explanation output",
            )

        if provider_dispatch_enabled is not False:
            return GateDecision(
                self.name,
                self.action_type,
                "FAILCLOSED",
                readiness,
                blocking_residuals=["provider_dispatch_enabled"],
                reason="provider dispatch must not be enabled for explanation output",
            )

        explanation_output = (
            payload.get("explanation_output")
            or payload.get("output")
            or payload.get("artifact")
            or {}
        )

        forbidden_keys = contains_forbidden_key(explanation_output)
        if forbidden_keys:
            return GateDecision(
                self.name,
                self.action_type,
                "FAILCLOSED",
                readiness,
                blocking_residuals=forbidden_keys,
                reason="forbidden output field detected in explanation output",
            )

        decision, missing = evaluate_readiness_vector(readiness)

        return GateDecision(
            gate_name=self.name,
            action_type=self.action_type,
            decision=decision,
            readiness_vector=readiness,
            missing_evidence=missing,
            blocking_residuals=missing,
            reason="ready" if decision == "READY" else "missing evidence or admissibility residuals",
        )
