from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'reports/v1_4'; out.mkdir(parents=True,exist_ok=True)
obj={'branch':'v1.4-final-release-manifest-and-tagging','successor':'v1.4R-final-release-smoke-and-archive','reason':'run final smoke/archive pass after tag readiness','runtime_authority_granted':False,'provider_dispatch_enabled':False}
path=out/'zant_llm_v1_4_successor_recommendation.json'; path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('ZANT_LLM_V1_4_SUCCESSOR_RECOMMENDATION_CREATED=True')
print('SUCCESSOR='+obj['successor'])
print('REPORT='+str(path))
