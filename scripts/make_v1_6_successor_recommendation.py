from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reports' / 'v1_6' / 'zant_llm_v1_6_successor_recommendation.json'
OUT.parent.mkdir(parents=True, exist_ok=True)
obj = {
  'version': 'v1.6',
  'branch': 'v1.6-runtime-observability-and-operator-dashboard',
  'successor': 'v1.6R-runtime-observability-audit-and-dashboard-hardening',
  'reason': 'v1.6 introduces operator dashboard outputs; v1.6R should audit and harden dashboard correctness before later expansion.',
  'runtime_authority_granted': False,
  'provider_dispatch_enabled': False
}
OUT.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('ZANT_LLM_V1_6_SUCCESSOR_RECOMMENDATION_CREATED=True')
print('SUCCESSOR=v1.6R-runtime-observability-audit-and-dashboard-hardening')
print(f'REPORT={OUT}')
