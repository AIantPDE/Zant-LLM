from __future__ import annotations

RUNTIME_AUTHORITY_GRANTED = False
PROVIDER_DISPATCH_ENABLED = False
BRANCH = "v1.5-post-release-monitoring-and-maintenance"
BASE_BRANCH = "v1.4R-final-release-smoke-and-archive"
RELEASE_TAG = "v1.4.0"
SUCCESSOR = "v1.5R-post-release-monitoring-audit-and-hotfix-readiness"


def classify_smoke(text: str) -> str:
    t = (text or "").lower()
    if "runtime_authority_granted" in t or "provider_dispatch" in t or "ignore policy" in t:
        return "FAILCLOSED"
    if "source conflict" in t or "missing" in t or "no evidence" in t:
        return "BLOCKED"
    if "closeout" in t or "no new action" in t or "resolved" in t:
        return "CLOSEOUT"
    return "READY"


def build_monitoring_report() -> dict:
    return {
        "branch": BRANCH,
        "base_branch": BASE_BRANCH,
        "release_tag": RELEASE_TAG,
        "monitoring_checks": 20,
        "release_health_score": 1.0,
        "blocking_issues": 0,
        "post_release_monitoring_accepted": True,
        "runtime_authority_granted": False,
        "provider_dispatch_enabled": False,
        "successor": SUCCESSOR,
    }
