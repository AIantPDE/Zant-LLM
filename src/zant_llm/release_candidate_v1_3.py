from pathlib import Path
import json, hashlib

BRANCH = 'v1.3-release-candidate-packaging'
BASE_BRANCH = 'v1.2-runtime-deployment-readiness'
SUCCESSOR = 'v1.3R-release-candidate-signoff-and-smoke'
RUNTIME_AUTHORITY_GRANTED = False
PROVIDER_DISPATCH_ENABLED = False


def read_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def evaluate_release_candidate(root: Path):
    data = read_json(root / 'data/trace_hix_v1_3/release_candidate_checks.json')
    checks = data['release_candidate_checks']
    passed = sum(1 for c in checks if c.get('status') == 'pass')
    total = len(checks)
    blocking = sum(1 for c in checks if c.get('blocking') and c.get('status') != 'pass')
    categories = {}
    for c in checks:
        categories[c['category']] = categories.get(c['category'], 0) + 1
    score = round(passed / total, 4) if total else 0.0
    accepted = (score == 1.0 and blocking == 0 and data['runtime_authority_granted'] is False and data['provider_dispatch_enabled'] is False)
    return {
        'report_version': 'zant_llm_v1_3_rc_packaging_report_v0',
        'branch': BRANCH,
        'base_branch': BASE_BRANCH,
        'rc_checks': total,
        'passed_checks': passed,
        'rc_score': score,
        'blocking_issues': blocking,
        'accepted': accepted,
        'category_counts': categories,
        'runtime_authority_granted': False,
        'provider_dispatch_enabled': False,
        'successor': SUCCESSOR,
    }


def build_artifact_inventory(root: Path):
    artifacts = []
    for rel in [
        'README.md',
        'GOVERNANCE.md',
        'SECURITY.md',
        'RELEASE_POLICY.md',
        'docs/V1_3_RELEASE_CANDIDATE_PACKAGING.md',
        'docs/RELEASE_CANDIDATE_CHECKLIST.md',
        'data/trace_hix_v1_3/release_candidate_checks.json',
        'schemas/zant_llm_v1_3_rc_packaging_report_v0.schema.json',
        'scripts/RUN_V1_3_ALL_LOCAL.ps1',
        'scripts/BUILD_V1_3_RELEASE_CANDIDATE_PACKAGE.ps1',
        'src/zant_llm/release_candidate_v1_3.py',
    ]:
        path = root / rel
        artifacts.append({'path': rel, 'exists': path.exists(), 'sha256': sha256_file(path) if path.exists() else None})
    return {
        'report_version': 'zant_llm_v1_3_artifact_inventory_v0',
        'branch': BRANCH,
        'artifact_count': len(artifacts),
        'artifacts': artifacts,
        'runtime_authority_granted': False,
        'provider_dispatch_enabled': False,
    }


def build_summary_markdown(report):
    return f"""# Zant-LLM v1.3 Release Candidate Summary

- Branch: `{BRANCH}`
- Base branch: `{BASE_BRANCH}`
- RC score: `{report['rc_score']}`
- Blocking issues: `{report['blocking_issues']}`
- Accepted: `{report['accepted']}`
- Runtime authority granted: `false`
- Provider dispatch enabled: `false`
- Successor: `{SUCCESSOR}`
"""
