# Creating optimizer file.

import numpy as np
from inject_fake_points import generate_cluster_points


def score_location(center, size=0.3, num_points=500):
    """
    Score a candidate attack location.
    A tighter cluster gets a better score.
    """
    center = np.array(center)
    fake_points = generate_cluster_points(center, size=size, num_points=num_points)

    distances = np.linalg.norm(fake_points - center, axis=1)

    # Smaller average distance equals to tighter cluster means better score.
    score = -np.mean(distances)

    return score, fake_points


# Finding the best location.
def find_best_location(
        x_range=(4, 10),
        y_range=(-3, 3),
        z_range=(-1, 1),
        trials=30,
        size=0.3,
        num_points=500
):
    best_score = -np.inf
    best_center = None
    best_fake_points = None

    for _ in range(trials):
        center = [
            np.random.uniform(*x_range),
            np.random.uniform(*y_range),
            np.random.uniform(*z_range)
        ]
        score, fake_points = score_location(center, size=size, num_points=num_points)

        if score > best_score:
            best_score = score
            best_center = center
            best_fake_points = fake_points
    return best_center, best_score, best_fake_points
