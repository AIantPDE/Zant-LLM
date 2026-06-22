from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ['VERSION','README.md','GOVERNANCE.md','SECURITY.md','configs/v1_2/runtime_config_template.json','data/trace_hix_v1_2/deployment_readiness_checks.json','src/zant_llm/deployment_readiness_v1_2.py','scripts/run_v1_2_stdlib_tests.py']
def main():
    for rel in REQUIRED:
        if not (ROOT/rel).exists():
            raise AssertionError(f'missing required file: {rel}')
    data=json.loads((ROOT/'data/trace_hix_v1_2/deployment_readiness_checks.json').read_text(encoding='utf-8'))
    assert len(data['checks'])==18
    assert data['runtime_authority_granted'] is False
    assert data['provider_dispatch_enabled'] is False
    print('[Zant-LLM v1.2] repository root:', ROOT)
    print('ZANT_LLM_V1_2_REPOSITORY_VALID=True')
    print('DEPLOYMENT_CHECKS=18')
    print('RUNTIME_AUTHORITY_GRANTED=False')
    print('PROVIDER_DISPATCH_ENABLED=False')
    return 0
if __name__=='__main__': raise SystemExit(main())
