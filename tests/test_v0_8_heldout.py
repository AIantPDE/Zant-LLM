from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from zant_llm.v0_8_dataset import load_heldout_eval
from zant_llm.gates.heldout_model_eval_gate_v0 import evaluate_heldout_case

def test_heldout_count():
    assert len(load_heldout_eval()) == 180

def test_decision_contract():
    for row in load_heldout_eval():
        assert evaluate_heldout_case(row) == row['expected_decision']
