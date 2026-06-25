"""Zant-LLM v1.5R post-release audit and hotfix readiness helpers."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Iterable, Mapping

from .governance import fail_closed_gate, governance_flags


@dataclass(frozen=True)
class AuditResult:
    release_health_score: float
    smoke_pass_rate: float
    audit_pass_rate: float
    hotfix_readiness_score: float
    regression_replay_pass_rate: float
    blocking_issues: int
    post_release_audit_accepted: bool
    hotfix_readiness_accepted: bool
    runtime_authority_granted: bool
    provider_dispatch_enabled: bool

    def to_dict(self) -> dict:
        return asdict(self)


def ratio_passed(rows: Iterable[Mapping]) -> float:
    rows = list(rows)
    if not rows:
        return 0.0
    passed = sum(1 for row in rows if bool(row.get("expected_pass", row.get("passed", False))))
    return round(passed / len(rows), 6)


def compute_audit_result(
    audit_checks: list[dict],
    smoke_cases: list[dict],
    hotfix_checks: list[dict],
    regression_cases: list[dict],
) -> AuditResult:
    flags = governance_flags()
    audit_rate = ratio_passed(audit_checks)
    smoke_rate = ratio_passed(smoke_cases)
    hotfix_rate = ratio_passed(hotfix_checks)
    regression_rate = ratio_passed(regression_cases)

    gate_failures = 0
    for row in list(audit_checks) + list(smoke_cases) + list(hotfix_checks) + list(regression_cases):
        if not fail_closed_gate(row).get("allowed", False):
            # A blocked probe is acceptable only when the row explicitly expects blocking.
            if row.get("expected_gate") != "blocked":
                gate_failures += 1

    blocking = sum(1 for row in audit_checks if row.get("severity") == "blocking" and not row.get("expected_pass", False))
    blocking += gate_failures

    release_health = round(min(audit_rate, smoke_rate, hotfix_rate, regression_rate), 6)
    accepted = (
        release_health == 1.0
        and blocking == 0
        and flags["runtime_authority_granted"] is False
        and flags["provider_dispatch_enabled"] is False
    )

    return AuditResult(
        release_health_score=release_health,
        smoke_pass_rate=smoke_rate,
        audit_pass_rate=audit_rate,
        hotfix_readiness_score=hotfix_rate,
        regression_replay_pass_rate=regression_rate,
        blocking_issues=blocking,
        post_release_audit_accepted=accepted,
        hotfix_readiness_accepted=accepted,
        runtime_authority_granted=flags["runtime_authority_granted"],
        provider_dispatch_enabled=flags["provider_dispatch_enabled"],
    )


def classify_hotfix_issue(issue: Mapping) -> dict:
    severity = str(issue.get("severity", "low")).lower()
    reproducible = bool(issue.get("reproducible", False))
    regression = bool(issue.get("regression", False))
    safety_related = bool(issue.get("safety_related", False))

    if safety_related or (severity in {"critical", "high"} and reproducible):
        lane = "hotfix_candidate"
    elif regression and reproducible:
        lane = "regression_replay_required"
    else:
        lane = "maintenance_backlog"

    return {
        "lane": lane,
        "requires_owner": lane != "maintenance_backlog",
        "runtime_authority_granted": False,
        "provider_dispatch_enabled": False,
    }
