# Uniform Disk Random Walk

What is the distribution of the position after many steps, each uniformly distributed on a disk of radius r? The notebook answers numerically: the uniform-disk density is discretised on a grid and the step distribution is convolved with itself repeatedly (`scipy.signal.convolve2d`), which is the density of the sum of i.i.d. steps. The mean and covariance of the result are measured and compared with a 2D Gaussian having the same moments, as predicted by the central limit theorem, and the L1 distance between the two is printed.

## How to run
Python 3 with `numpy`, `scipy`, `matplotlib`. Open `random_variables.ipynb` in Jupyter and run all cells (30 convolutions by default).

## Notes
- The grid is 30 r wide with 20 intervals per radius; the error is dominated by discretisation of the disk edge.
