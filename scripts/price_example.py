import sys
from pathlib import Path
from src.mbs_lab.engine import price_one

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage  python scripts/price_example.py configs/example_config.yaml")
        raise SystemExit(1)
    cfg = sys.argv[1]
    Path("models").mkdir(exist_ok=True)
    out = price_one(cfg)
    print("pricing complete")
    print(out)
