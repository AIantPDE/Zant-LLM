BRANCH = 'v1.4-final-release-manifest-and-tagging'
BASE_BRANCH = 'v1.3R-release-candidate-signoff-and-smoke'
RECOMMENDED_TAG = 'v1.4.0'
SUCCESSOR = 'v1.4R-final-release-smoke-and-archive'
RUNTIME_AUTHORITY_GRANTED = False
PROVIDER_DISPATCH_ENABLED = False

def build_final_release_report(checks):
    total = len(checks)
    passed = sum(1 for c in checks if c.get('status') == 'pass')
    blocking = [c for c in checks if c.get('required') and c.get('status') != 'pass']
    score = 1.0 if total == 0 else passed / total
    return {'report_version':'zant_llm_v1_4_final_release_report_v0','branch':BRANCH,'base_branch':BASE_BRANCH,'recommended_tag':RECOMMENDED_TAG,'final_checks':total,'passed_checks':passed,'final_release_score':round(score,6),'blocking_issues':len(blocking),'final_release_accepted':len(blocking)==0 and score>=1.0,'runtime_authority_granted':False,'provider_dispatch_enabled':False}

def tag_recommendation():
    return {'recommended_tag':RECOMMENDED_TAG,'tag_command':'git tag -a '+RECOMMENDED_TAG+' -m "Zant-LLM '+RECOMMENDED_TAG+' final runtime governance release"','push_command':'git push origin '+RECOMMENDED_TAG,'runtime_authority_granted':False,'provider_dispatch_enabled':False}
