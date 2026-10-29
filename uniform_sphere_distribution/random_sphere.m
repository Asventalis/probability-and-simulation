% Generate n random points on a sphere of radius 1 in 3D coordinates
n = 10000; % Number of points
points = uniform_sphere(n);

% Compute the sum of the reciprocal of the distance squared from all other points
distances = pdist2(points, points); % Pairwise distances
weights = sum(distances < 0.2 & distances > 0, 2); % Count points with distance less than 0.2, excluding self-distances

% Plot the points with color based on weights
figure;
scatter3(points(:, 1), points(:, 2), points(:, 3), 80, weights, 'filled');
caxis([n/1000 n/50]); % Fix the color axis range
xlabel('X');
ylabel('Y');
zlabel('Z');
title('Random Points on the Unit Sphere Colored by Reciprocal Distance Sum');
colorbar; % Add a colorbar to indicate the weights
grid on;
camva(10); % Avoid automatic scaling with rotation of 3d graph
camproj('perspective'); % Perspective projection


function [points] = not_uniform_sphere(n)
    if nargin < 1
        n = 1; % Default value for n
    end

    % Generate n random theta and alpha values
    theta = 2 * pi * rand(n, 1) - pi; % Random angles in [-pi, pi]
    alpha = pi * rand(n, 1) - pi/2; % Random angles in [-pi/2, pi/2]

    % Convert spherical coordinates to Cartesian coordinates
    x = cos(alpha) .* cos(theta);
    y = cos(alpha) .* sin(theta);
    z = sin(alpha);

    % Combine x, y, z into points matrix
    points = [x, y, z];
end

function [points] = xyz_uniform_sphere(n)
    if nargin < 1
        n = 1; % Default value for n
    end

    % Generate random points in 3D space
    x = 2 * rand(n, 1) - 1; % Random values in [-1, 1]
    y = 2 * rand(n, 1) - 1; % Random values in [-1, 1]
    z = 2 * rand(n, 1) - 1; % Random values in [-1, 1]

    % Normalize the vectors to lie on the unit sphere
    norms = sqrt(x.^2 + y.^2 + z.^2);
    x = x ./ norms;
    y = y ./ norms;
    z = z ./ norms;

    % Combine x, y, z into points matrix
    points = [x, y, z];
end

function [points] = uniform_sphere(n)
    if nargin < 1
        n = 1; % Default value for n
    end

    % Generate n random theta and alpha values
    theta = 2 * pi * rand(n, 1) - pi; % Random angles in [-pi, pi]
    alpha = asin(2 * rand(n, 1) - 1); % Random angles in [-pi/2, pi/2] for uniform distribution on a sphere

    % Convert spherical coordinates to Cartesian coordinates
    x = cos(alpha) .* cos(theta);
    y = cos(alpha) .* sin(theta);
    z = sin(alpha);

    % Combine x, y, z into points matrix
    points = [x, y, z];
end