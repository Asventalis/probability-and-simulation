# Moving Points Colour Field

An animation of n points drifting and bouncing inside the unit square, each carrying an RGB colour that itself wanders randomly (rotated in colour space by a random Rodrigues rotation each frame). The background is coloured by inverse-distance weighting of the points' colours with a very high exponent, so each pixel takes the colour of its nearest point and the image approaches a Voronoi diagram that deforms in real time. `voronoilight.py` replaces the normalised weights with an additive 1/(k0 + k1 d + k2 d^2) attenuation, so points act like coloured lights fading into black.

## How to run
Python 3 with `numpy`, `scipy`, `matplotlib`: `python voronoi.py` and enter the number of points.

## Notes
- The field is recomputed on a 300x300 grid every frame in pure numpy, so frame rate drops with many points.
- `scipy.spatial.Voronoi` is imported but not used; the cells emerge from the weighting.
