import numpy as np


def generate_fake_points(box: dict, num_points: int = 200) -> np.ndarray:
    """
    Generate fake LiDAR points inside a 3d box.

    box keys: x_min, x_max, y_min, y_max, z_min, z_max
    """
    x = np.random.uniform(box["x_min"], box["x_max"], num_points)
    y = np.random.uniform(box["y_min"], box["y_max"], num_points)
    z = np.random.uniform(box["z_min"], box["z_max"], num_points)

    return np.column_stack((x, y, z))


# Creating denser cluster like object (Structured points looks more like object than random points.)
def generate_cluster_points(center, size=1.0, num_points=300):
    """
    Generate clustered fake points around a center.
    """
    x = np.random.normal(center[0], size, num_points)
    y = np.random.normal(center[1], size, num_points)
    z = np.random.normal(center[2], size, num_points)

    return np.column_stack((x, y, z))


def inject_fake_points(original_points: np.ndarray, fake_points: np.ndarray) -> np.ndarray:
    """
    Combine original points with the fake points.
    """
    return np.vstack((original_points, fake_points))
