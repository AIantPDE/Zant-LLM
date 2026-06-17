from __future__ import annotations
import argparse, json, hashlib, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from zant_llm.v0_6R_calibration import summarize, recommend_successor

def load_jsonl(path: Path): return [json.loads(x) for x in path.read_text(encoding='utf-8').splitlines() if x.strip()]
def write_json(path: Path, obj): path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
def write_jsonl(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as f:
        for r in rows: f.write(json.dumps(r, ensure_ascii=False)+'\n')
def sha256(path: Path) -> str: h=hashlib.sha256(); h.update(path.read_bytes()); return h.hexdigest()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--input', default=str(ROOT/'data/trace_hix_v0_6R/v0_6_realworld_eval_snapshot_300.jsonl')); args=ap.parse_args()
    inp=Path(args.input); rows=load_jsonl(inp); summary=summarize(rows); rec=recommend_successor(summary)
    candidates=[r for r in rows if r.get('needs_calibration_review')]
    train_candidates=[r for r in rows if r.get('family') in ('blocked_source_conflict','blocked_unsupported_claim','failclosed_counterfactual_overreach')][:60]
    report={'report_version':'zant_llm_v0_6R_calibration_report_v1','branch':'v0.6R-realworld-eval-calibration','input_file':str(inp),'input_sha256':sha256(inp),**summary,'successor_recommendation':rec,'runtime_authority_granted':False,'provider_dispatch_enabled':False}
    write_json(ROOT/'reports/v0_6R/zant_llm_v0_6R_calibration_report.json', report)
    write_json(ROOT/'reports/v0_6R/zant_llm_v0_6R_error_bucket_summary.json', {'mismatch_count':summary['mismatch_count'],'governance_leakage_count':summary['governance_leakage_count'],'family_counts':summary['family_counts'],'runtime_authority_granted':False,'provider_dispatch_enabled':False})
    write_json(ROOT/'reports/v0_6R/zant_llm_v0_6R_successor_recommendation.json', rec)
    write_jsonl(ROOT/'data/trace_hix_v0_6R/calibration_candidates.jsonl', candidates)
    write_jsonl(ROOT/'data/trace_hix_v0_6R/v0_7_training_candidates.jsonl', train_candidates)
    print('ZANT_LLM_V0_6R_CALIBRATION_ANALYZED=True')
    print(f'TOTAL={summary["total"]}')
    print(f'PASS_RATE={summary["pass_rate"]}')
    for k,v in summary['decision_counts'].items(): print(f'{k}_COUNT={v}')
    print(f'SUCCESSOR={rec["successor"]}')
    print('RUNTIME_AUTHORITY_GRANTED=False')
    print('PROVIDER_DISPATCH_ENABLED=False')
    return 0
if __name__ == '__main__': raise SystemExit(main())
