from pathlib import Path
from zant_llm.baseline import read_jsonl, train_baseline, predict
ROOT = Path(__file__).resolve().parents[1]

def test_seed_count():
    rows = read_jsonl(ROOT / "data" / "seed" / "zant_llm_v0_1_seed_30.jsonl")
    assert len(rows) == 30

def test_train_and_predict():
    model = train_baseline(ROOT / "data" / "seed" / "zant_llm_v0_1_seed_30.jsonl")
    row = read_jsonl(ROOT / "data" / "eval" / "zant_llm_v0_1_eval_10.jsonl")[0]
    pred = predict(model, row)
    assert "prediction" in pred
    assert pred["runtime_authority_granted"] is False
