import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"src"))
from zant_llm.v0_3_dataset import build_sft_dataset

def main() -> int:
    n1 = build_sft_dataset(ROOT/"data/trace_hix_v0_3/trace_hix_v0_3_train_cases_60.jsonl", ROOT/"data/trace_hix_v0_3/sft_train_60.jsonl")
    n2 = build_sft_dataset(ROOT/"data/trace_hix_v0_3/trace_hix_v0_3_eval_cases_12.jsonl", ROOT/"data/trace_hix_v0_3/sft_eval_12.jsonl")
    print("ZANT_LLM_V0_3_SFT_DATASET_BUILT=True")
    print(f"SFT_TRAIN_COUNT={n1}")
    print(f"SFT_EVAL_COUNT={n2}")
    return 0
if __name__ == "__main__": raise SystemExit(main())
