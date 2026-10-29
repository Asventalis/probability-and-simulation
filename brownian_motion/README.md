# Geometric Brownian Motion

Simulates N paths of a geometric Brownian motion dX = mu X dt + sigma X dW with the Euler-Maruyama scheme: Gaussian increments dW ~ N(0, dt) are drawn with numpy and the recursion X[t+1] = X[t] + mu X[t] dt + sigma X[t] dW[t] is applied step by step. The notebook then plots the ensemble of trajectories.

## How to run
Python 3 with `numpy` and `matplotlib`. Open `brownian_motion.ipynb` in Jupyter and run all cells; parameters (mu, sigma, X0, N paths, horizon T, L steps) are set at the top of the second cell.

## Notes
- Written while following the LSE Summer School course on Monte Carlo methods (see `LSE_code`).
- With the default mu = 10 and sigma = 20 the paths explode quickly; lower values give the usual stock-price-like picture.
