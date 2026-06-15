from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    total = 0
    for test_file in sorted((ROOT / "tests").glob("test_*.py")):
        module = load_module(test_file)
        for name in sorted(dir(module)):
            if name.startswith("test_"):
                fn = getattr(module, name)
                if callable(fn):
                    fn()
                    print(f"PASS {test_file.name}::{name}")
                    total += 1
    print(f"TRACE_HIX_V0_2_STDLIB_TESTS_PASSED=True total={total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
