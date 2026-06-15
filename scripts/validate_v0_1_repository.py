import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "README.md",
    "GOVERNANCE.md",
    "TRAINING_LANE_REGISTRY.md",
    "configs/v0_1_train_config.json",
    "data/seed/zant_llm_v0_1_seed_30.jsonl",
    "data/eval/zant_llm_v0_1_eval_10.jsonl",
    "scripts/train_v0_1_baseline.py",
    "scripts/eval_v0_1_baseline.py",
]

RUNTIME_FLAGS_THAT_MUST_STAY_FALSE = [
    "zant_llm_provider_connected",
    "provider_dispatch_enabled",
    "runtime_authority_granted",
]

TEXT_FILE_SUFFIXES = {".md", ".py", ".json", ".jsonl", ".ps1", ".yml", ".yaml", ".txt"}
SKIP_DIRS = {".git", ".venv", "__pycache__", ".pytest_cache", ".ruff_cache", "outputs"}


def read_jsonl_count(path: Path) -> int:
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def assert_required_files() -> None:
    missing = [p for p in REQUIRED if not (ROOT / p).exists()]
    if missing:
        raise FileNotFoundError("Missing required files: " + ", ".join(missing))


def assert_config_runtime_flags_false() -> None:
    config = json.loads((ROOT / "configs/v0_1_train_config.json").read_text(encoding="utf-8"))
    flags = config.get("forbidden_runtime_flags", {})
    for flag in RUNTIME_FLAGS_THAT_MUST_STAY_FALSE:
        if flags.get(flag) is not False:
            raise AssertionError(f"{flag} must be False in configs/v0_1_train_config.json")


def assert_dataset_counts() -> None:
    seed_count = read_jsonl_count(ROOT / "data/seed/zant_llm_v0_1_seed_30.jsonl")
    eval_count = read_jsonl_count(ROOT / "data/eval/zant_llm_v0_1_eval_10.jsonl")
    if seed_count != 30:
        raise AssertionError(f"Expected 30 seed lines, got {seed_count}")
    if eval_count != 10:
        raise AssertionError(f"Expected 10 eval lines, got {eval_count}")


def assert_no_runtime_true_patterns() -> None:
    # 只拦截真正的 True/true 赋值或 JSON 布尔值，避免验证脚本因为自身列出禁用词而误报。
    patterns = [
        re.compile(rf'["\\\']?{re.escape(flag)}["\\\']?\\s*[:=]\\s*(?:true|True|TRUE)\\b')
        for flag in RUNTIME_FLAGS_THAT_MUST_STAY_FALSE
    ]
    for path in ROOT.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if not path.is_file() or path.suffix.lower() not in TEXT_FILE_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in patterns:
            if pattern.search(text):
                raise AssertionError(f"Forbidden runtime True pattern found in {path}")


def main() -> int:
    assert_required_files()
    assert_config_runtime_flags_false()
    assert_dataset_counts()
    assert_no_runtime_true_patterns()
    print("ZANT_LLM_V0_1_REPOSITORY_VALID=True")
    print("SEED_COUNT=30")
    print("EVAL_COUNT=10")
    print("RUNTIME_AUTHORITY_GRANTED=False")
    print("PROVIDER_DISPATCH_ENABLED=False")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
