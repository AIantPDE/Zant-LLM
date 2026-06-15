"""Run v0.1 tests with Python standard library only.

This fallback avoids requiring pytest on a fresh Windows/PowerShell machine.
It discovers test_*.py files under tests/, imports them, and executes all
module-level functions whose names start with test_.
"""
from __future__ import annotations

import importlib.util
import inspect
import sys
from pathlib import Path


def load_module(path: Path):
    name = "zant_llm_v0_1_test_" + path.stem
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load test module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    src = root / "src"
    tests_dir = root / "tests"
    sys.path.insert(0, str(src))
    sys.path.insert(0, str(root))

    if not tests_dir.exists():
        print("ZANT_LLM_V0_1_STDLIB_TESTS_SKIPPED=True reason=no_tests_dir")
        return 0

    total = 0
    failures: list[str] = []

    for test_file in sorted(tests_dir.glob("test_*.py")):
        module = load_module(test_file)
        for name, obj in sorted(vars(module).items()):
            if name.startswith("test_") and inspect.isfunction(obj):
                total += 1
                try:
                    obj()
                    print(f"PASS {test_file.name}::{name}")
                except Exception as exc:  # noqa: BLE001 - simple local fallback runner
                    failures.append(f"FAIL {test_file.name}::{name}: {exc!r}")
                    print(failures[-1])

    if failures:
        print(f"ZANT_LLM_V0_1_STDLIB_TESTS_PASSED=False total={total} failed={len(failures)}")
        return 1

    print(f"ZANT_LLM_V0_1_STDLIB_TESTS_PASSED=True total={total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
