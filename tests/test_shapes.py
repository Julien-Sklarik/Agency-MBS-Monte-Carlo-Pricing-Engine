import numpy as np
from src.mbs_lab.rates import simulate_hull_white_paths

def test_rate_shapes():
    r = simulate_hull_white_paths(n_paths=10, n_steps=12, dt=1.0, a=0.1, sigma=0.01, r0=0.03, theta=0.03)
    assert r.shape == (10, 12)
