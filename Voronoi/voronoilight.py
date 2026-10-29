import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

def main():
    try:
        n = int(input("Enter the number of points: "))
    except ValueError:
        print("Please enter a valid integer.")
        return

    grid_res = 300                    
    velocities_magnitude = 0.3
    color_velocities_magnitude = 0
    fps = 100                 
    
    # color_strength = 7

    radius = 0.2
    k0 = 1
    k1 = 2/radius
    k2 = 1/radius**2
    
    xi = np.linspace(0, 1, grid_res)
    yi = np.linspace(0, 1, grid_res)
    X, Y = np.meshgrid(xi, yi)

    positions = np.random.rand(n, 2)
    velocities = (np.random.rand(n, 2) - 0.5)
    velocities *= velocities_magnitude / np.linalg.norm(velocities, axis=1)[:, None]
    colors = np.random.rand(n, 3)
    color_velocities = (np.random.rand(n, 3) - 0.5)
    color_velocities = color_velocities_magnitude * color_velocities / np.linalg.norm(color_velocities, axis=1)[:, None]

    fig, ax = plt.subplots(figsize=(8, 8))
    grid_shape = (grid_res, grid_res, 3)
    color_image = np.zeros(grid_shape)

    # Instead of the normalized weighted average,
    # we now add contributions so that farther pixels are darker.
    for i, (px, py) in enumerate(positions):
        d = np.sqrt((X - px)**2 + (Y - py)**2)
        # w = 1 / np.power(d + k0, color_strength)
        w = 1 / (k0 + k1 * d + k2 * d**2)
        color_image[:, :, 0] += w * colors[i, 0]
        color_image[:, :, 1] += w * colors[i, 1]
        color_image[:, :, 2] += w * colors[i, 2]
    color_image = np.clip(color_image, 0, 1)

    im = ax.imshow(color_image, extent=(0, 1, 0, 1), origin='lower')

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("Moving Points with Light‑like Attenuation")

    old_time = time.time()
    current_time = time.time()

    def update(frame):
        nonlocal positions, velocities, colors, color_velocities, old_time, current_time

        old_time = current_time
        current_time = time.time()
        dt = current_time - old_time

        positions += velocities * dt
        mask_x_low = positions[:, 0] <= 0
        mask_x_high = positions[:, 0] >= 1
        velocities[mask_x_low | mask_x_high, 0] *= -1
        positions[:, 0] = np.clip(positions[:, 0], 0, 1)
        mask_y_low = positions[:, 1] <= 0
        mask_y_high = positions[:, 1] >= 1
        velocities[mask_y_low | mask_y_high, 1] *= -1
        positions[:, 1] = np.clip(positions[:, 1], 0, 1)

        angle = np.random.uniform(-0.1, 0.1) * dt
        axis = np.random.randn(3)
        axis /= np.linalg.norm(axis)
        K = np.array([[0, -axis[2], axis[1]],
                      [axis[2], 0, -axis[0]],
                      [-axis[1], axis[0], 0]])
        R_mat = np.eye(3) + np.sin(angle) * K + (1 - np.cos(angle)) * (K @ K)
        color_velocities = np.dot(color_velocities, R_mat)
        colors += color_velocities * dt
        mask = (colors <= 0) | (colors >= 1)
        color_velocities[mask] *= -1
        colors = np.clip(colors, 0, 1)

        # Recompute the background by summing contributions.
        color_image = np.zeros(grid_shape)
        for i, (px, py) in enumerate(positions):
            d = np.sqrt((X - px)**2 + (Y - py)**2)
            # w = 1 / np.power(d + k0, color_strength)
            w = 1 / (k0 + k1 * d + k2 * d**2)
            color_image[:, :, 0] += w * colors[i, 0]
            color_image[:, :, 1] += w * colors[i, 1]
            color_image[:, :, 2] += w * colors[i, 2]
        # Divide by number of points
        # color_image /= n
        color_image = np.clip(color_image, 0, 1)
        im.set_array(color_image)
        return im,

    interval = 1000 / fps
    ani = animation.FuncAnimation(fig, update, interval=interval, blit=True)
    plt.show()

if __name__ == "__main__":
    main()
