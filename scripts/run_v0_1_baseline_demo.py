from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from zant_llm.baseline import generate_template_explanation  # noqa: E402
from zant_llm.schema import validate_record  # noqa: E402


def main() -> int:
    seed_path = ROOT / "data/seed/zant_llm_v0_1_seed_30.jsonl"
    out_dir = ROOT / "outputs"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "v0_1_baseline_demo_outputs.jsonl"

    count = 0
    with seed_path.open("r", encoding="utf-8") as rf, out_path.open("w", encoding="utf-8", newline="\n") as wf:
        for line in rf:
            if not line.strip():
                continue
            record = json.loads(line)
            validate_record(record)
            output = generate_template_explanation(record)
            wf.write(json.dumps({"id": record["id"], "output": output}, ensure_ascii=False) + "\n")
            count += 1

    print("ZANT_LLM_V0_1_BASELINE_DEMO_DONE=True")
    print(f"OUTPUT={out_path}")
    print(f"COUNT={count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
