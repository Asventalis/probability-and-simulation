# Cereal Box Problem

How many cereal boxes do you expect to buy before collecting all 6 different prizes? The notebook answers the coupon-collector question by modelling the number of distinct prizes owned as an absorbing Markov chain: from state i the next box is new with probability (n-i)/n. Using sympy, the fundamental matrix N = (I - Q)^-1 of the transient part gives the expected absorption time t = N * 1 exactly as a rational number, and the construction is generalised to any n.

## How to run
Python 3 with `sympy`. Open `cereal.ipynb` in Jupyter and run the two cells; `expected_steps(n)` returns the exact expected number of boxes.

## Notes
- For n = 6 the result is 147/10 = 14.7 boxes, matching the harmonic-number formula n * H_n.
