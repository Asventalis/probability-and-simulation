# Pairing 20 People

Counts the number of ways to split 20 people into 10 unordered pairs. The notebook computes it in two equivalent ways: as the product of binomial coefficients C(20,2) * C(18,2) * ... * C(2,2) divided by 10! (to remove the ordering of the pairs), and as the closed form 20! / (2^10 * 10!), using only hand-written `factorial` and `binomial` functions with exact integer arithmetic.

## How to run
Python 3, no dependencies. Open `binomial_sum.ipynb` in Jupyter and run the cells. `demo.py` is a placeholder.

## Notes
- Both methods give 654,729,075, which is the double factorial 19!!.
- The project was scaffolded with `uv` (`pyproject.toml`), but nothing beyond the standard library is used.
