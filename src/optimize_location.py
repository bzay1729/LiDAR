import numpy as np
from inject_fake_points import generate_cluster_points


def score_location(center, original_points, size=0.3, num_points=500):
    """
    Score a candidate fake-point location based on how close
    the generated fake points are to the real point cloud.

    Smaller average distance to real points = stronger overlap
    with the scene = better attack score.
    """
    center = np.array(center)
    fake_points = generate_cluster_points(center, size=size, num_points=num_points)

    distances = []

    # For each fake point, compute its distance to the nearest real point
    for fp in fake_points:
        d = np.min(np.linalg.norm(original_points - fp, axis=1))
        distances.append(d)

    # Smaller distance is better, so negate mean distance
    score = -np.mean(distances)

    return score, fake_points


def find_best_location(
        original_points,
        x_range=(4, 10),
        y_range=(-3, 3),
        z_range=(-1, 1),
        trials=30,
        size=0.3,
        num_points=500
):
    """
    Random-search optimization:
    - sample candidate centers
    - generate fake cluster at each center
    - score candidate using real-scene overlap
    - keep the best one
    """
    best_score = -np.inf
    best_center = None
    best_fake_points = None

    for _ in range(trials):
        center = [
            np.random.uniform(*x_range),
            np.random.uniform(*y_range),
            np.random.uniform(*z_range)
        ]

        score, fake_points = score_location(
            center=center,
            original_points=original_points,
            size=size,
            num_points=num_points
        )

        if score > best_score:
            best_score = score
            best_center = center
            best_fake_points = fake_points

    return best_center, best_score, best_fake_points
