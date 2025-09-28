import sys
from pathlib import Path
from src.mbs_lab.engine import run_training

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage  python scripts/train_models.py configs/example_config.yaml")
        raise SystemExit(1)
    cfg = sys.argv[1]
    Path("models").mkdir(exist_ok=True)
    res = run_training(cfg)
    print("training complete")
    print(res)
