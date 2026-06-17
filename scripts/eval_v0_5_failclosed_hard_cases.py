import json, sys, hashlib, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from zant_llm.gates import ExplanationAdmissibilityGate, TrainingSampleAdmissibilityGate, FollowUpAdmissibilityGate, CounterfactualAdmissibilityGate, LaneSuccessorAdmissibilityGate, HardCaseFailClosedGate
G = {c.__name__: c() for c in [ExplanationAdmissibilityGate, TrainingSampleAdmissibilityGate, FollowUpAdmissibilityGate, CounterfactualAdmissibilityGate, LaneSuccessorAdmissibilityGate, HardCaseFailClosedGate]}

def read(p):
    return [json.loads(x) for x in Path(p).read_text(encoding='utf-8').splitlines() if x.strip()]

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    path = ROOT / 'data/trace_hix_v0_5/hard_eval_60.jsonl'
    cases = read(path)
    rows = []
    passed = 0
    counts = {'FAILCLOSED': 0, 'BLOCKED': 0, 'CLOSEOUT': 0, 'READY': 0}
    for c in cases:
        gd = G[c['gate']].evaluate(c['input'])
        ok = gd.decision == c['expected_decision']
        passed += int(ok)
        counts[gd.decision] += 1
        rows.append({'case_id': c['case_id'], 'family': c['family'], 'gate': c['gate'], 'expected': c['expected_decision'], 'actual': gd.decision, 'ok': ok, 'reason': gd.reason})
    report = {
        'report_version': 'zant_llm_v0_5_failclosed_eval_v1',
        'branch': 'v0.5-adversarial-hard-cases-and-failclosed-eval',
        'total': len(cases),
        'passed': passed,
        'pass_rate': passed / len(cases),
        'counts': counts,
        'eval_data_sha256': sha(path),
        'runtime_authority_granted': False,
        'provider_dispatch_enabled': False,
        'rows': rows,
        'created_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
    }
    out = ROOT / 'reports/v0_5/zant_llm_v0_5_failclosed_eval_report.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('ZANT_LLM_V0_5_EVALUATED=True')
    print('MODE=adversarial-hard-cases-failclosed')
    print(f'HARD_CASE_PASS_RATE={report["pass_rate"]}')
    print(f'FAILCLOSED_COUNT={counts["FAILCLOSED"]}')
    print(f'BLOCKED_COUNT={counts["BLOCKED"]}')
    print(f'CLOSEOUT_COUNT={counts["CLOSEOUT"]}')
    print(f'REPORT={out}')
    print('RUNTIME_AUTHORITY_GRANTED=False')
    print('PROVIDER_DISPATCH_ENABLED=False')
    return 0 if passed == len(cases) else 1

if __name__ == '__main__':
    raise SystemExit(main())
