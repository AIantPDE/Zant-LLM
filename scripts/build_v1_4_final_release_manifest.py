from pathlib import Path
import json, hashlib, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from zant_llm.final_release_v1_4 import build_final_release_report, tag_recommendation, BRANCH, BASE_BRANCH
checks=json.loads((ROOT/'data/trace_hix_v1_4/final_release_checks.json').read_text(encoding='utf-8'))
branch_index=json.loads((ROOT/'data/trace_hix_v1_4/final_branch_index.json').read_text(encoding='utf-8'))
report=build_final_release_report(checks); tag=tag_recommendation(); out=ROOT/'reports/v1_4'; out.mkdir(parents=True,exist_ok=True)
(out/'zant_llm_v1_4_final_release_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(out/'zant_llm_v1_4_tag_recommendation.json').write_text(json.dumps(tag,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(out/'zant_llm_v1_4_branch_index.json').write_text(json.dumps(branch_index,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
notes=(ROOT/'data/trace_hix_v1_4/release_notes_seed.md').read_text(encoding='utf-8')
(out/'zant_llm_v1_4_release_notes.md').write_text(notes,encoding='utf-8')
gh='# Zant-LLM '+tag['recommended_tag']+'\n\nFinal runtime governance release.\n\n- branch: '+BRANCH+'\n- base: '+BASE_BRANCH+'\n- final_release_score: '+str(report['final_release_score'])+'\n- blocking_issues: '+str(report['blocking_issues'])+'\n- runtime_authority_granted: false\n- provider_dispatch_enabled: false\n'
(out/'zant_llm_v1_4_github_release_draft.md').write_text(gh,encoding='utf-8')
sha=[]
for p in sorted(ROOT.rglob('*')):
    if p.is_file() and '.git' not in p.parts and '__pycache__' not in p.parts and p.suffix!='.pyc':
        sha.append(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(ROOT).as_posix())
(out/'zant_llm_v1_4_sha256_summary.txt').write_text('\n'.join(sha)+'\n',encoding='utf-8')
print('ZANT_LLM_V1_4_FINAL_RELEASE_PACKAGE_BUILT=True')
print('FINAL_RELEASE_SCORE='+str(report['final_release_score']))
print('BLOCKING_ISSUES='+str(report['blocking_issues']))
print('FINAL_RELEASE_ACCEPTED='+str(report['final_release_accepted']))
print('RECOMMENDED_TAG='+tag['recommended_tag'])
print('RUNTIME_AUTHORITY_GRANTED=False')
print('PROVIDER_DISPATCH_ENABLED=False')
