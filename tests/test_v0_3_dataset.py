from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"src"))
from zant_llm.v0_3_dataset import load_jsonl

def test_train_count(): assert len(load_jsonl(ROOT/"data/trace_hix_v0_3/trace_hix_v0_3_train_cases_60.jsonl")) == 60
def test_eval_count(): assert len(load_jsonl(ROOT/"data/trace_hix_v0_3/trace_hix_v0_3_eval_cases_12.jsonl")) == 12
