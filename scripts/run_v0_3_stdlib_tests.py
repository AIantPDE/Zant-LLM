import importlib.util, inspect, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"src"))
def load(path):
    spec=importlib.util.spec_from_file_location(path.stem, path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
def main():
    total=0
    for path in sorted((ROOT/"tests").glob("test_*.py")):
        mod=load(path)
        for name,obj in sorted(vars(mod).items()):
            if name.startswith("test_") and callable(obj) and not inspect.signature(obj).parameters:
                obj(); total += 1; print(f"PASS {path.name}::{name}")
    print(f"ZANT_LLM_V0_3_STDLIB_TESTS_PASSED=True total={total}")
    return 0
if __name__ == "__main__": raise SystemExit(main())
