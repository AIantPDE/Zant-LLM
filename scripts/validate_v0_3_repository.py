from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md", "GOVERNANCE.md", "TRAINING_LANE_REGISTRY.md",
    "configs/v0_3_gemma4_qlora_config.json",
    "data/trace_hix_v0_3/trace_hix_v0_3_train_cases_60.jsonl",
    "data/trace_hix_v0_3/trace_hix_v0_3_eval_cases_12.jsonl",
    "scripts/train_v0_3_gemma4_qlora.py", "scripts/eval_v0_3_gemma4_qlora.py",
]
def count_jsonl(path: Path) -> int:
    return sum(1 for line in path.open("r", encoding="utf-8") if line.strip())
def main() -> int:
    for rel in REQUIRED:
        if not (ROOT/rel).exists(): raise AssertionError(f"missing {rel}")
    train_count = count_jsonl(ROOT/"data/trace_hix_v0_3/trace_hix_v0_3_train_cases_60.jsonl")
    eval_count = count_jsonl(ROOT/"data/trace_hix_v0_3/trace_hix_v0_3_eval_cases_12.jsonl")
    if train_count != 60: raise AssertionError(train_count)
    if eval_count != 12: raise AssertionError(eval_count)
    print("ZANT_LLM_V0_3_REPOSITORY_VALID=True")
    print(f"TRAIN_CASES={train_count}")
    print(f"EVAL_CASES={eval_count}")
    print("RUNTIME_AUTHORITY_GRANTED=False")
    print("PROVIDER_DISPATCH_ENABLED=False")
    return 0
if __name__ == "__main__": raise SystemExit(main())
