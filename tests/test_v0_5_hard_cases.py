from pathlib import Path
def test_hard_case_files_exist():
    assert Path('data/trace_hix_v0_5/hard_train_240.jsonl').exists()
