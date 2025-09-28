import numpy as np

def simulate_hull_white_paths(n_paths: int, n_steps: int, dt: float, a: float, sigma: float, r0: float, theta: float) -> np.ndarray:
    r = np.zeros((n_paths, n_steps), dtype=float)
    r[:, 0] = r0
    sqrt_dt = np.sqrt(dt)
    for t in range(1, n_steps):
        z = np.random.normal(size=n_paths)
        drift_term = a * np.subtract(theta, r[:, t - 1]) * dt
        diff_term = sigma * sqrt_dt * z
        r[:, t] = r[:, t - 1] + drift_term + diff_term
    return r

def discount_factors_from_paths(r_paths: np.ndarray, dt: float) -> np.ndarray:
    # r_paths shape n_paths by n_steps
    # returns same shape array of discount factors from zero to each step
    n_paths, n_steps = r_paths.shape
    df = np.ones_like(r_paths)
    for t in range(1, n_steps):
        df[:, t] = df[:, t - 1] * np.exp(-r_paths[:, t] * dt)
    return df
