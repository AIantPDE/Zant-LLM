from pathlib import Path
from zant_llm.v0_4_dataset import load_jsonl, to_sft
ROOT=Path(__file__).resolve().parents[1]
def test_train_count(): assert len(load_jsonl(ROOT/'data/trace_hix_v0_4/train_cases_180.jsonl'))==180
def test_eval_count(): assert len(load_jsonl(ROOT/'data/trace_hix_v0_4/eval_cases_45.jsonl'))==45
def test_sft_format(): assert 'OUTPUT_JSON' in to_sft(load_jsonl(ROOT/'data/trace_hix_v0_4/train_cases_180.jsonl')[0])['text']
