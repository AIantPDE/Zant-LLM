from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    'VERSION','README.md','GOVERNANCE.md','SECURITY.md',
    'configs/v1_3/rc_packaging_config_template.json',
    'data/trace_hix_v1_3/release_candidate_checks.json',
    'src/zant_llm/release_candidate_v1_3.py',
    'scripts/run_v1_3_stdlib_tests.py'
]
def main():
    for rel in REQUIRED:
        if not (ROOT / rel).exists():
            raise AssertionError(f'missing required file: {rel}')
    data = json.loads((ROOT/'data/trace_hix_v1_3/release_candidate_checks.json').read_text(encoding='utf-8'))
    assert data['branch'] == 'v1.3-release-candidate-packaging'
    assert data['base_branch'] == 'v1.2-runtime-deployment-readiness'
    assert len(data['release_candidate_checks']) == 20
    assert data['runtime_authority_granted'] is False
    assert data['provider_dispatch_enabled'] is False
    print('[Zant-LLM v1.3] repository root:', ROOT)
    print('ZANT_LLM_V1_3_REPOSITORY_VALID=True')
    print('RC_CHECKS=20')
    print('RUNTIME_AUTHORITY_GRANTED=False')
    print('PROVIDER_DISPATCH_ENABLED=False')
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
