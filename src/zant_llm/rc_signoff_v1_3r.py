from pathlib import Path
import json, hashlib, time, uuid

BRANCH = 'v1.3R-release-candidate-signoff-and-smoke'
BASE_BRANCH = 'v1.3-release-candidate-packaging'
SUCCESSOR = 'v1.4-final-release-manifest-and-tagging'
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


def infer_smoke(text: str):
    t = (text or '').lower()
    if not t.strip():
        return 'BLOCKED', 'empty_or_missing_input'
    if 'runtime_authority_granted=true' in t or 'provider_dispatch_enabled=true' in t or 'ignore policy' in t or 'hidden injection' in t or 'bypass governance' in t:
        return 'FAILCLOSED', 'repair_failclosed'
    if 'closeout' in t or 'no further action' in t or 'followup not needed' in t:
        return 'CLOSEOUT', 'closeout_route'
    if 'missing evidence' in t or 'source conflict' in t or 'malformed' in t or 'conflict' in t:
        return 'BLOCKED', 'evidence_blocked'
    if 'verified' in t or 'bounded' in t or 'sufficient evidence' in t:
        return 'READY', 'bounded_ready'
    return 'BLOCKED', 'fallback_blocked'


def evaluate_signoff(root: Path):
    data = read_json(root / 'data/trace_hix_v1_3R/rc_signoff_checks.json')
    checks = data['rc_signoff_checks']
    passed = sum(1 for c in checks if c.get('status') == 'pass')
    total = len(checks)
    blocking = sum(1 for c in checks if c.get('blocking') and c.get('status') != 'pass')
    categories = {}
    for c in checks:
        categories[c['category']] = categories.get(c['category'], 0) + 1
    score = round(passed / total, 4) if total else 0.0
    accepted = score == 1.0 and blocking == 0 and data['runtime_authority_granted'] is False and data['provider_dispatch_enabled'] is False
    return {
        'report_version':'zant_llm_v1_3R_signoff_report_v0',
        'branch':BRANCH,
        'base_branch':BASE_BRANCH,
        'signoff_checks':total,
        'passed_checks':passed,
        'signoff_score':score,
        'blocking_issues':blocking,
        'accepted':accepted,
        'category_counts':categories,
        'runtime_authority_granted':False,
        'provider_dispatch_enabled':False,
        'successor':SUCCESSOR,
    }


def evaluate_smoke(root: Path):
    rows=[]
    path = root / 'data/trace_hix_v1_3R/rc_smoke_cases_12.jsonl'
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.strip():
            row=json.loads(line)
            decision, parse_mode = infer_smoke(row.get('text',''))
            ok = decision == row['expected_decision']
            rows.append({
                'id':row['id'],
                'expected_decision':row['expected_decision'],
                'decision':decision,
                'parse_mode':parse_mode,
                'ok':ok,
                'request_id':str(uuid.uuid4()),
                'ts_unix':time.time(),
                'runtime_authority_granted':False,
                'provider_dispatch_enabled':False,
            })
    total=len(rows)
    passed=sum(1 for r in rows if r['ok'])
    rate=round(passed/total,4) if total else 0.0
    return {
        'report_version':'zant_llm_v1_3R_smoke_report_v0',
        'branch':BRANCH,
        'base_branch':BASE_BRANCH,
        'smoke_cases':total,
        'passed_cases':passed,
        'smoke_pass_rate':rate,
        'accepted':rate == 1.0,
        'results':rows,
        'runtime_authority_granted':False,
        'provider_dispatch_enabled':False,
    }


def build_artifact_inventory(root: Path):
    rels = [
        'README.md','GOVERNANCE.md','SECURITY.md','RELEASE_POLICY.md',
        'docs/V1_3R_RELEASE_CANDIDATE_SIGNOFF_AND_SMOKE.md','docs/RC_SIGNOFF_AND_SMOKE_CHECKLIST.md',
        'data/trace_hix_v1_3R/rc_signoff_checks.json','data/trace_hix_v1_3R/rc_smoke_cases_12.jsonl',
        'schemas/zant_llm_v1_3R_signoff_report_v0.schema.json',
        'scripts/RUN_V1_3R_ALL_LOCAL.ps1','scripts/BUILD_V1_3R_SIGNOFF_AND_SMOKE.ps1',
        'src/zant_llm/rc_signoff_v1_3r.py',
    ]
    arts=[]
    for rel in rels:
        p=root/rel
        arts.append({'path':rel,'exists':p.exists(),'sha256':sha256_file(p) if p.exists() else None})
    return {
        'report_version':'zant_llm_v1_3R_artifact_inventory_v0',
        'branch':BRANCH,
        'artifact_count':len(arts),
        'artifacts':arts,
        'runtime_authority_granted':False,
        'provider_dispatch_enabled':False,
    }


def build_summary_markdown(signoff, smoke):
    return f'''# Zant-LLM v1.3R Release Candidate Signoff Summary

- Branch: `{BRANCH}`
- Base branch: `{BASE_BRANCH}`
- Signoff score: `{signoff['signoff_score']}`
- Smoke pass rate: `{smoke['smoke_pass_rate']}`
- Blocking issues: `{signoff['blocking_issues']}`
- Signoff accepted: `{signoff['accepted']}`
- Smoke accepted: `{smoke['accepted']}`
- Runtime authority granted: `false`
- Provider dispatch enabled: `false`
- Successor: `{SUCCESSOR}`
'''
