import numpy as np


def save_kitti_bin(points_xyz: np.ndarray, output_path: str):
    """
    Save point cloud in KITTI .bin format.
    KITTI expects each point as: x, y, z, intensity
    If only x, y, z are available, intensity is set to 0.
    """
    if points_xyz.shape[1] != 3:
        raise ValueError("Input points must have shape (N, 3) for x, y, z.")

    num_points = points_xyz.shape[0]

    # Add intensity column filled with zeros
    intensity = np.zeros((num_points, 1), dtype=np.float32)

    points_xyzi = np.hstack((points_xyz.astype(np.float32), intensity))

    # Save as binary
    points_xyzi.tofile(output_path)

    print(f"Saved attacked point cloud to: {output_path}")
    print(f"Saved shape: {points_xyzi.shape}")