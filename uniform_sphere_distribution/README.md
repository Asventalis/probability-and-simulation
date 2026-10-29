# Uniform Points on a Sphere

Compares three ways of generating random points on the unit sphere and shows visually why the naive one is wrong. `not_uniform_sphere` draws longitude and latitude uniformly, which clusters points near the poles; `uniform_sphere` draws the latitude as asin(2u - 1) so that the surface area element is uniform (inverse transform sampling of the sin density); `xyz_uniform_sphere` normalises uniform points from the cube (also non-uniform, denser along the cube diagonals). Each point is coloured by the number of neighbours within a fixed distance, so density differences are visible at a glance.

## How to run
MATLAB: run `random_sphere.m`; change the call at the top (`uniform_sphere(n)`) to one of the other generators to compare.

## Notes
- Uses `pdist2`, so n = 10,000 points need about 800 MB for the distance matrix.
