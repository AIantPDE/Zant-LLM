from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_training_script_has_qlora_terms():
    t=(ROOT/"scripts/train_v0_3_gemma4_qlora.py").read_text(encoding="utf-8")
    assert "BitsAndBytesConfig" in t and "LoraConfig" in t
