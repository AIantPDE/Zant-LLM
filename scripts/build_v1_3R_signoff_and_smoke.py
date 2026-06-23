from pathlib import Path
import json, sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from zant_llm.rc_signoff_v1_3r import evaluate_signoff, evaluate_smoke, build_artifact_inventory, build_summary_markdown

def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def main():
    signoff=evaluate_signoff(ROOT)
    smoke=evaluate_smoke(ROOT)
    inv=build_artifact_inventory(ROOT)
    write_json(ROOT/'reports/v1_3R/zant_llm_v1_3R_rc_signoff_report.json', signoff)
    write_json(ROOT/'reports/v1_3R/zant_llm_v1_3R_smoke_report.json', smoke)
    write_json(ROOT/'reports/v1_3R/zant_llm_v1_3R_artifact_inventory.json', inv)
    (ROOT/'reports/v1_3R/zant_llm_v1_3R_signoff_summary.md').write_text(build_summary_markdown(signoff, smoke), encoding='utf-8')
    print('ZANT_LLM_V1_3R_SIGNOFF_AND_SMOKE_BUILT=True')
    print('SIGNOFF_SCORE='+str(signoff['signoff_score']))
    print('SMOKE_PASS_RATE='+str(smoke['smoke_pass_rate']))
    print('BLOCKING_ISSUES='+str(signoff['blocking_issues']))
    print('RC_SIGNOFF_ACCEPTED='+str(signoff['accepted'] and smoke['accepted']))
    print('REPORT='+str(ROOT/'reports/v1_3R/zant_llm_v1_3R_rc_signoff_report.json'))
    print('RUNTIME_AUTHORITY_GRANTED=False')
    print('PROVIDER_DISPATCH_ENABLED=False')
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
