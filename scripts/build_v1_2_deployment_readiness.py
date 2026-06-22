from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from zant_llm.deployment_readiness_v1_2 import evaluate_readiness, build_artifact_inventory
def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
def main():
    report=evaluate_readiness(ROOT)
    inventory=build_artifact_inventory(ROOT)
    write_json(ROOT/'reports/v1_2/zant_llm_v1_2_deployment_readiness_report.json', report)
    write_json(ROOT/'reports/v1_2/zant_llm_v1_2_artifact_inventory.json', inventory)
    print('ZANT_LLM_V1_2_DEPLOYMENT_READINESS_BUILT=True')
    print('READINESS_SCORE='+str(report['readiness_score']))
    print('BLOCKING_ISSUES='+str(report['blocking_issues']))
    print('DEPLOYMENT_READINESS_ACCEPTED='+str(report['accepted']))
    print('REPORT='+str(ROOT/'reports/v1_2/zant_llm_v1_2_deployment_readiness_report.json'))
    print('RUNTIME_AUTHORITY_GRANTED=False')
    print('PROVIDER_DISPATCH_ENABLED=False')
    return 0
if __name__=='__main__': raise SystemExit(main())
