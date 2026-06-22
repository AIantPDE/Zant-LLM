from pathlib import Path
import json, sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from zant_llm.release_candidate_v1_3 import evaluate_release_candidate, build_artifact_inventory, build_summary_markdown

def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def main():
    report = evaluate_release_candidate(ROOT)
    inventory = build_artifact_inventory(ROOT)
    write_json(ROOT/'reports/v1_3/zant_llm_v1_3_rc_packaging_report.json', report)
    write_json(ROOT/'reports/v1_3/zant_llm_v1_3_artifact_inventory.json', inventory)
    (ROOT/'reports/v1_3/zant_llm_v1_3_release_candidate_summary.md').write_text(build_summary_markdown(report), encoding='utf-8')
    print('ZANT_LLM_V1_3_RELEASE_CANDIDATE_PACKAGE_BUILT=True')
    print('RC_SCORE='+str(report['rc_score']))
    print('BLOCKING_ISSUES='+str(report['blocking_issues']))
    print('RELEASE_CANDIDATE_ACCEPTED='+str(report['accepted']))
    print('REPORT='+str(ROOT/'reports/v1_3/zant_llm_v1_3_rc_packaging_report.json'))
    print('RUNTIME_AUTHORITY_GRANTED=False')
    print('PROVIDER_DISPATCH_ENABLED=False')
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
