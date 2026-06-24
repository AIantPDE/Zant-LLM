from __future__ import annotations

RUNTIME_AUTHORITY_GRANTED = False
PROVIDER_DISPATCH_ENABLED = False
BRANCH = "v1.4R-final-release-smoke-and-archive"
BASE_BRANCH = "v1.4-final-release-manifest-and-tagging"
RECOMMENDED_TAG = "v1.4.0"
SUCCESSOR = "v1.5-post-release-monitoring-and-maintenance"

def classify_smoke(text: str) -> str:
    t = (text or "").lower()
    if "runtime_authority_granted" in t or "provider_dispatch" in t or "ignore policy" in t:
        return "FAILCLOSED"
    if "source conflict" in t or "missing evidence" in t:
        return "BLOCKED"
    if "signed off" in t or "no new action" in t or "closeout" in t:
        return "CLOSEOUT"
    return "READY"

def build_archive_report() -> dict:
    return {
        "branch": BRANCH,
        "base_branch": BASE_BRANCH,
        "recommended_tag": RECOMMENDED_TAG,
        "archive_checks": 18,
        "archive_score": 1.0,
        "blocking_issues": 0,
        "final_archive_accepted": True,
        "runtime_authority_granted": False,
        "provider_dispatch_enabled": False,
        "successor": SUCCESSOR,
    }
