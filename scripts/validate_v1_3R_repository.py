from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    'VERSION','README.md','GOVERNANCE.md','SECURITY.md',
    'configs/v1_3R/signoff_config_template.json',
    'data/trace_hix_v1_3R/rc_signoff_checks.json',
    'data/trace_hix_v1_3R/rc_smoke_cases_12.jsonl',
    'src/zant_llm/rc_signoff_v1_3r.py',
    'scripts/run_v1_3R_stdlib_tests.py'
]
def main():
    for rel in REQUIRED:
        if not (ROOT / rel).exists():
            raise AssertionError(f'missing required file: {rel}')
    data=json.loads((ROOT/'data/trace_hix_v1_3R/rc_signoff_checks.json').read_text(encoding='utf-8'))
    assert data['branch'] == 'v1.3R-release-candidate-signoff-and-smoke'
    assert data['base_branch'] == 'v1.3-release-candidate-packaging'
    assert len(data['rc_signoff_checks']) == 24
    assert data['runtime_authority_granted'] is False
    assert data['provider_dispatch_enabled'] is False
    print('[Zant-LLM v1.3R] repository root:', ROOT)
    print('ZANT_LLM_V1_3R_REPOSITORY_VALID=True')
    print('SIGNOFF_CHECKS=24')
    print('SMOKE_CASES=12')
    print('RUNTIME_AUTHORITY_GRANTED=False')
    print('PROVIDER_DISPATCH_ENABLED=False')
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
