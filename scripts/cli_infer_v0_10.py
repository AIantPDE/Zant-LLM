import argparse, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from zant_llm.inference_contract_v0_10 import infer_contract
ap=argparse.ArgumentParser()
ap.add_argument('--text', required=True)
ap.add_argument('--raw-model-output', default='')
args=ap.parse_args()
print(json.dumps(infer_contract(args.text, args.raw_model_output or None), ensure_ascii=False))
